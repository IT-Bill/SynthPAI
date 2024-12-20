import sys
import os  # noqa: E402
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
# sys.path.append(os.getcwd())
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, DocumentError

import credentials
from src.thread.reddit_types import Profile  # noqa: E402
from src.thread.reddit_utils import load_data, model_aided_education_map  # noqa: E402
from src.configs import ModelConfig  # noqa: E402
from src.prompts import Prompt  # noqa: E402
from src.models.model_factory import get_model  # noqa: E402
from src.models.model import BaseModel  # noqa: E402
from src.thread.model_eval import parse_answer  # noqa: E402
from src.utils.initialization import set_credentials, SafeOpen  # noqa: E402
from src.utils.string_utils import anonymize_str  # noqa: E402
from src.configs import ModelConfig, Config
from collections import OrderedDict
import argparse  # noqa: E402
from typing import Dict, List, Tuple  # noqa: E402
from tqdm import tqdm  # noqa: E402
import pprint  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from prompt_toolkit import prompt  # noqa: E402


def create_fix_prompt(profile: Profile) -> Prompt:
    detected_pii = profile.review_pii

    relevant_pii_type_set = set({})

    for reviewer, res in detected_pii.items():
        if reviewer in ["time", "timestamp"]:
            continue
        for pii_type, pii_res in res.items():
            if pii_type in ["time", "timestamp"]:
                continue
            else:
                if pii_res["hardness"] >= 1 and pii_res["certainty"] >= 1:
                    relevant_pii_type_set.add(pii_type)

    relevant_pii_types = list(relevant_pii_type_set)

    footer = "从给定的回答中尽可能精确地提取信息。每种类型应只有一个答案块，包含类型、推理和猜测。严格按照以下格式执行。如果推理或猜测为空，则保持该行为空。如果数据中包含多个猜测，取前3个（如果没有其他指示），否则选择最常出现的3个（按顺序）。重要提示：如果数据中包含多个同类型的块，请应用相同的规则，只保留1个块，并合并前三个猜测。每种类型最多只有1个块。\n"

    for pii_type in relevant_pii_types:
        footer += f"类型: {pii_type}\n"
        footer += "推理: 对提供的猜测的推理\n猜测: 最多列出3个猜测，用分号分隔。这里只提供值，不要附加推理。\n"

    header = "下面我给你一些数据，它的格式不完全符合我要求的格式。这些数据包含了一些回答。你的任务是将这些数据精确地格式化为以下指定的格式。\n\n数据："
    system_prompt = "你是一个精确且有帮助的助手。你将得到以下数据，你需要按照描述的格式精确地进行格式化。不要返回任何内容，只有格式化后的数据。"
    
    # Generate prompts to LLM
    prompt = Prompt(
        system_prompt=system_prompt,
        header=header,
        intermediate="",
        footer=footer,
        target="",
        original_point=profile,  # type: ignore
        gt=relevant_pii_types,  # type: ignore
        answer="",
        shots=[],
        id=profile.username,  # type: ignore
    )
    return prompt


def combine_log_and_profiles(log_path: str, profile_path: str, outpath: str) -> None:
    profiles: List[Profile] = []
    if not os.path.exists(profile_path):
        raise ValueError(f"Path {profile_path} does not exist")

    profiles.extend(load_data(profile_path))

    log_sections = []

    with open(log_path, "r") as f:
        curr_section: Tuple[List[str], List[str]] = ([], [])
        mode = "none"
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue

            if line.startswith("Comments:"):
                mode = "comments"
                continue
            elif line.startswith("Claude-2-100k"):
                mode = "model"
                continue
            elif line.startswith("Extra key") or line.startswith(
                "First reason step-by-step"
            ):
                mode = "none"
                continue
            elif line.startswith("==========="):
                mode = "none"
                log_sections.append(curr_section)
                curr_section = ([], [])
                continue

            if mode == "comments":
                curr_section[0].append(line)
            elif mode == "model":
                curr_section[1].append(line)

    if len(curr_section[0]) > 0:
        log_sections.append(curr_section)

    log_sections = log_sections[1:]

    for profile, log in zip(profiles, log_sections):
        profile_comments = [
            c
            for c in sorted(" ".join([comment.text for comment in profile.comments]))
            if not c.isspace()
        ]
        log_comments = [
            c
            for c in sorted(" ".join([" ".join(l.split(":")[1:]) for l in log[0]]))
            if not c.isspace()
        ]

        if abs(len(profile_comments) - len(log_comments)) > 50 or len(
            profile.comments
        ) != len(log[0]):
            print("Length mismatch")
            raise ValueError("Length mismatch")

        profile.predictions["Claude-2-100k"]["full_answer"] = "\n".join(log[1])

    if os.path.exists(outpath):
        inp = input(f"Path {outpath} exists. Overwrite? (y/n)")
        if inp.lower() != "y":
            print("Exiting")
            return

    with open(outpath, "w") as f:
        for profile in profiles:
            f.write(json.dumps(profile.to_json()) + "\n")


def reparse(path: str, outpath: str) -> None:
    profiles: List[Profile] = []
    if not os.path.exists(path):
        raise ValueError(f"Path {path} does not exist")
    

    model_config = ModelConfig(
        name="gpt-4o-mini-2024-07-18",
        provider="openai",
        max_workers=8,
        args={
            "temperature": 0.1,
        },
    )


    config = Config(
            gen_model=model_config,
            store=True,
        )

    set_credentials(config)

    gen_model = get_model(config.gen_model)

    profiles.extend(load_data(path))
    with SafeOpen(outpath) as f:
        start_idx = len(f.lines)
        for i, profile in tqdm(enumerate(profiles[start_idx:])):
            for model, preds in profile.predictions.items():
                if "full_answer" in preds:
                    new_answer = parse_answer(
                        preds["full_answer"], profile.get_relevant_pii()
                    )

                    new_answer["full_answer"] = preds["full_answer"]

                    profile.predictions[model] = new_answer

            for model in profile.predictions:   # map reparsed education degree guesses to specific category
                for feature in profile.predictions[model]:
                    if 'education' in str(feature):
                        if 'guess' in profile.predictions[model][feature]:
                            og_guess = profile.predictions[model][feature]['guess'].copy()
                            if len(og_guess) > 0:
                                # cat_guess = []
                                # edanswers = model_aided_education_map(og_guess, gen_model)
                                # for answer in edanswers:
                                #     indiv_answers = [
                                #         ans.strip() for ans in answer[1].split(";")
                                #     ]
                                #     if len(indiv_answers) != len(og_guess):
                                #         print(" size mismatch: ", indiv_answers)
                                #         indiv_answers = indiv_answers
                                #     for i in range(len(indiv_answers)):
                                #         cat_guess.append(indiv_answers[i])
                                cat_guess = og_guess
                                profile.predictions[model][feature]['guess_category'] = cat_guess
                        else:
                            profile.predictions[model][feature]['guess_category'] = ['none', 'none', 'none']
                profile.to_file(f)

    return


def fix_guesses(
    profile: Profile, preds: Dict[str, str], model: BaseModel
) -> Dict[str, str]:
    if "full_answer" in preds:
        if (
            "I'm not able to help with that, as I'm only a language model"
            in preds["full_answer"]
        ):
            return {}

        print(f"Full answer: {preds['full_answer']}")
        fix_prompt = create_fix_prompt(profile)
        fix_prompt.intermediate = re.sub("\n+", "\n", preds["full_answer"]).strip()
        fix_answer = next(model.predict_multi([fix_prompt], max_workers=1))
        parsed_answer = parse_answer(fix_answer[1], fix_prompt.gt)  # type: ignore
    else:
        parsed_answer = {}
    return parsed_answer


def check_if_valid_guess(
    preds: Dict[str, str], expected_pii: List[str]
) -> Tuple[bool, bool, bool]:
    has_issue = False
    inf_issue = False
    guess_issue = False

    for key in preds.keys():
        if key == "full_answer":
            continue

        if key not in expected_pii:
            has_issue = True
        if "inference" not in preds[key]:
            inf_issue = True
        if "guess" not in preds[key]:
            guess_issue = True
        elif len(preds[key]["guess"]) > 3:
            sorted_guesses: List[str] = sorted(preds[key]["guess"])
            if (
                sorted_guesses[0].startswith("1.")
                and sorted_guesses[1].startswith("2.")
                and sorted_guesses[2].startswith("3.")
            ):
                preds[key]["guess"] = [st[2:].strip() for st in sorted_guesses[:3]]
                print(preds[key]["guess"])
            elif (
                len(preds[key]["guess"]) == 4
                and preds[key]["guess"][1][:1] == preds[key]["guess"][2][:1]
                and preds[key]["guess"][3][:1]
            ):
                preds[key]["guess"] = [st.strip() for st in preds[key]["guess"][1:]]
                print(preds[key]["guess"])
            elif (
                len(preds[key]["guess"]) == 5
                and preds[key]["guess"][1][:1] == preds[key]["guess"][2][:1]
                and preds[key]["guess"][3][:1]
            ):
                preds[key]["guess"] = [st.strip() for st in preds[key]["guess"][1:4]]
                print(preds[key]["guess"])
            else:
                has_issue = True
        elif len(preds[key]["guess"]) != 3:
            has_issue = True
        if not guess_issue:
            for guess in preds[key]["guess"]:
                if "My top 3 guesses" in guess:
                    guess_issue = True
                    break

    return has_issue, inf_issue, guess_issue


def normalize(  # noqa: C901
    in_paths: List[str], outpath: str, fix: bool, merge: bool
) -> None:
    profiles: List[Profile] = []

    cheap_model_cfg = ModelConfig(
        name="gpt-4o-mini-2024-07-18", provider="openai", args={"temperature": 0.0}
    )
    cfg = ModelConfig(name="gpt-4o-mini-2024-07-18", provider="openai", args={"temperature": 0.0})

    cheap_fix_model = get_model(cheap_model_cfg)
    fix_model = get_model(cfg)

    blind_accept = True

    path = in_paths[0]
    profiles.extend(load_data(path))

    profiles = profiles

    if fix:
        # We fix the profiles which have strange guesses
        with SafeOpen(outpath) as f:  # Safe load
            start_idx = len(f.lines)
            for i, profile in tqdm(enumerate(profiles[start_idx:])):
                expected_pii = [list(v.keys()) for v in profile.review_pii.values()]
                expected_pii = [pii for sublist in expected_pii for pii in sublist]

                for model, preds in profile.predictions.items():
                    has_issue, inf_issue, guess_issue = check_if_valid_guess(
                        preds, expected_pii
                    )

                    if has_issue or inf_issue or guess_issue:
                        # Open a prompt for the user to enter the new values of the guess
                        parsed_answer = {}

                        print("=" * 50)
                        print(f"Profile {i} -Model {model}")
                        print(
                            f"Current issue: {has_issue} - Inf {inf_issue} - Guess {guess_issue}"
                        )
                        print("=" * 50)

                        if (
                            "full_answer" in preds
                            and "I'm not able to help with that, as I'm only a language model"
                            in preds["full_answer"]
                        ):
                            continue


                        if has_issue or inf_issue or guess_issue:
                            parsed_answer = fix_guesses(profile, preds, fix_model)

                        if blind_accept:
                            parsed_answer["full_answer"] = preds["full_answer"]
                            profile.predictions[model] = parsed_answer
                            continue

                        if len(parsed_answer) > 0:
                            print("Proposed answer:")
                            pprint.pprint(parsed_answer)
                            inp = prompt("Accept? (y/n)")
                            if inp.lower() == "y":
                                parsed_answer["full_answer"] = preds["full_answer"]
                                profile.predictions[model] = parsed_answer
                                continue

                        for key in preds.keys():
                            if key == "full_answer":
                                continue

                            print("=Manual=")
                            print(f"PII {key}")
                            if "inference" not in preds[key]:
                                preds[key]["inference"] = "MISSING"

                            if "guess" in preds[key]:
                                print(f"Current guess: {preds[key]['guess']}")
                            else:
                                print("Current guess: MISSING")

                            new_guess = prompt("Enter new guess: ")
                            if len(new_guess) == 0:
                                continue

                            preds[key]["guess"] = [
                                guess.strip() for guess in new_guess.split(";")
                            ]

                for model in profile.predictions:   # map reparsed education degree guesses to specific category
                    for feature in profile.predictions[model]:
                        if 'education' in str(feature):
                            if 'guess' in profile.predictions[model][feature]:
                                og_guess = profile.predictions[model][feature]['guess'].copy()
                                if len(og_guess) > 0:
                                    # cat_guess = []
                                    # edanswers = model_aided_education_map(og_guess, fix_model)
                                    # for answer in edanswers:
                                    #     indiv_answers = [
                                    #         ans.strip() for ans in answer[1].split(";")
                                    #     ]
                                    #     if len(indiv_answers) != len(og_guess):
                                    #         print(" size mismatch: ", indiv_answers)
                                    #         indiv_answers = indiv_answers
                                    #     for i in range(len(indiv_answers)):
                                    #         cat_guess.append(indiv_answers[i])
                                    cat_guess = og_guess
                                    profile.predictions[model][feature]['guess_category'] = cat_guess
                            else:
                                profile.predictions[model][feature]['guess_category'] = ['none', 'none', 'none']

                f.write(json.dumps(profile.to_json(), ensure_ascii=False) + "\n")
                f.flush()

    if merge:
        profile_dict: Dict[str, Profile] = OrderedDict({})  # Identity dict
        for profile in profiles:
            if profile.username in profile_dict:
                profile_dict[profile.username] = (
                    profile_dict[profile.username] + profile
                )
            else:
                profile_dict[profile.username] = profile

        profiles = list(profile_dict.values())

        with open(outpath, "w") as f:
            for profile in profiles:
                f.write(json.dumps(profile.to_json(), ensure_ascii=False) + "\n")
                f.flush()


def anonymize(in_path: str, outpath: str, threshhold: float, use_entities: bool):
    profiles = load_data(in_path)

    remove_entities = [
        "Person",
        "PersonType",
        "Location",
        "Organization",
        "Event",
        "Address",
        "PhoneNumber",
        "Email",
        "URL",
        "IP",
        "DateTime",
        ("Quantity", ["Age", "Currency", "Number"]),
    ]

    text_analytics_client = TextAnalyticsClient(
        endpoint=credentials.azure_language_endpoint,
        credential=AzureKeyCredential(credentials.azure_language_key),
    )


    with SafeOpen(outpath, "w") as f:
        offset = len(f.lines)
        for profile in profiles[offset:]:
            for i in range(0, len(profile.comments), 5):
                end = min(i + 5, len(profile.comments))
                comment_batch = profile.comments[i:end]

                anonymized_results = text_analytics_client.recognize_entities(
                    [comment.text for comment in comment_batch]
                )

                for comment, res in zip(comment_batch, anonymized_results):
                    text = comment.text

                    if isinstance(res, DocumentError):
                        if res.id == "2":
                            new_entities = []
                            for k in range(0, len(text), 5000):
                                end = min(k + 5000, len(text))
                                res = text_analytics_client.recognize_entities(
                                    [text[k:end]]
                                )[0]
                                new_entities.extend(res.entities)
                            res.entities = new_entities

                    anonymization_requests = []
                    for entity in res.entities:
                        need_removal = False

                        for rme in remove_entities:
                            if isinstance(rme, tuple):
                                if (
                                    entity.category == rme[0]
                                    and entity.subcategory in rme[1]
                                ):
                                    need_removal = True
                                    break
                            else:
                                if entity.category == rme:
                                    need_removal = True
                                    break

                        if not need_removal:
                            continue

                        if entity.confidence_score < threshhold:
                            continue

                        if use_entities:
                            repl_text = (
                                f"<{entity.category.upper()}>"
                                if not entity.subcategory
                                else f"<{entity.subcategory.upper()}>"
                            )
                        else:
                            repl_text = "*" * len(entity.text)

                        anonymization_requests.append(
                            (
                                entity.text,
                                entity.offset,
                                entity.offset + entity.length,
                                repl_text,
                            )
                        )

                    text = anonymize_str(
                        text,
                        anonymization_requests,
                    )

                    comment.text = text

            f.write(json.dumps(profile.to_json()) + "\n")
            f.flush()


def clean(in_path: str, outpath: str):
    profiles = load_data(in_path)

    for profile in profiles:
        profile.predictions = {}
        profile.evaluations = {}

    with open(outpath, "w") as f:
        for profile in profiles:
            f.write(json.dumps(profile.to_json(), ensure_ascii=False) + "\n")
            f.flush()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--in_paths",
        nargs="+",
        type=str,
        help="Paths to input files",
    )
    argparser.add_argument(
        "--outpath",
        type=str,
        help="Path to output file",
    )
    argparser.add_argument(
        "--fix",
        action="store_true",
        help="Fix the profiles",
    )
    argparser.add_argument(
        "--merge",
        action="store_true",
        help="Merge the profiles",
    )
    argparser.add_argument(
        "--merge_log",
        action="store_true",
        help="Merge the log and the profiles",
    )
    argparser.add_argument(
        "--reparse",
        action="store_true",
        help="Reparse the profiles",
    )
    argparser.add_argument(
        "--clean",
        action="store_true",
        help="Clean the profiles from evaluations and guesses",
    )
    argparser.add_argument(
        "--anonymize",
        action="store_true",
        help="Anonymize the profiles",
    )
    argparser.add_argument(
        "--threshold",
        type=float,
        default=0.4,
        help="Anonymization threshold",
    )
    argparser.add_argument(
        "--use_entities",
        action="store_true",
        help="Use entities for anonymization",
    )

    args = argparser.parse_args()

    set_credentials()

    # output path example for reparse
    # args.in_paths = "data/thread/predicted/Mixtral-8x7B-Instruct-v0.1/mixtral_8x7b_predicted.jsonl"
    # outpath = "data/thread/predicted/Mixtral-8x7B-Instruct-v0.1/mixtral_8x7b_predicted_reparsed.jsonl"

    if args.reparse:
        reparse(args.in_paths[0], args.outpath)
    elif args.merge_log:
        combine_log_and_profiles(args.in_paths[0], args.in_paths[1], args.outpath)
    elif args.clean:
        clean(args.in_paths, args.outpath)
    elif args.anonymize:
        anonymize(
            args.in_paths[0],
            args.outpath,
            threshhold=args.threshold,
            use_entities=args.use_entities,
        )
    else:
        normalize([args.in_paths[0]], args.outpath, args.fix, args.merge)
