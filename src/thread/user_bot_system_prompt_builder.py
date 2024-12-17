def build_user_bot_system_prompt(
    prompt_skeleton: str,
    profile: dict,
    writing_style: str,
    min_comment_len,
    max_comment_len,
    ct,
) -> str:
    """
    Takes a parameterized prompt skeleton for the user bot and a profile dictionary
    and return the filled out prompt skeleton, ready to use for the bot.

    :param prompt_skeleton: A string with parameters <param> matching the keys in the dictionary,
        This skeleton is filled out to generate the system prompt.
    :param profile: A dictionary containing the personal information of the profile that is to be
        impersonated by the user bot.
    :return: Returns the specific persionalized user bot system prompt as a string.
    """
    final_prompt = prompt_skeleton
    for key, value in profile.items():
        # if key == "education":
        #     if value.startswith("studying"):
        #         final_prompt = final_prompt.replace(f"<{key}>", f"are {value}")
        #     else:
        #         final_prompt = final_prompt.replace(f"<{key}>", f"hold a {value}")
        if key == "education":
            final_prompt = final_prompt.replace(f"<{key}>", f"{value}")
        
        elif key == "city_country":
            try: 
                city, country = value.split(", ")
            except:
                city = value
                country = "中国"
            final_prompt = final_prompt.replace(f"<city>", str(city))
            final_prompt = final_prompt.replace(f"<country>", str(country))
        else:
            final_prompt = final_prompt.replace(f"<{key}>", str(value))
        final_prompt = final_prompt.replace("<writing_style>", str(writing_style))
        final_prompt = final_prompt.replace("<min_comment_len>", str(min_comment_len))
        final_prompt = final_prompt.replace("<max_comment_len>", str(max_comment_len))
        if ct == True:
            final_prompt = final_prompt.replace(
                "<critic_type>",
                "You are always very critical and disagreeing with others there.",
            )
        else:
            final_prompt = final_prompt.replace("<critic_type>", "")
    return final_prompt


def build_author_bot_system_prompt(prompt_skeleton: str, profile: dict) -> str:
    """
    Takes a parameterized prompt skeleton for the user bot and a profile dictionary
    and return the filled out prompt skeleton, ready to use for the bot.

    :param prompt_skeleton: A string with parameters <param> matching the keys in the dictionary,
        This skeleton is filled out to generate the system prompt.
    :param profile: A dictionary containing the personal information of the profile that is to be
        impersonated by the user bot.
    :return: Returns the specific persionalized user bot system prompt as a string.
    """
    final_prompt = prompt_skeleton
    for key, value in profile.items():
        if key == "education":
            # if value.startswith("studying"):
            #     final_prompt = final_prompt.replace(f"<{key}>", f"are {value}")
            # else:
            #     final_prompt = final_prompt.replace(f"<{key}>", f"hold a {value}")
            final_prompt = final_prompt.replace(f"<{key}>", f"{value}")
        elif key == "city_country":
            try: 
                city, country = value.split(", ")
            except:
                city = value
                country = "中国"
            final_prompt = final_prompt.replace(f"<city>", str(city))
            final_prompt = final_prompt.replace(f"<country>", str(country))
        else:
            final_prompt = final_prompt.replace(f"<{key}>", str(value))
    return final_prompt


def build_checker_bot_system_prompt(
    prompt_skeleton: str, profile: dict, topic: str
) -> str:
    """
    Takes a parameterized prompt skeleton for the user bot and a profile dictionary
    and return the filled out prompt skeleton, ready to use for the bot.

    :param prompt_skeleton: A string with parameters <param> matching the keys in the dictionary,
        This skeleton is filled out to generate the system prompt.
    :param profile: A dictionary containing the personal information of the profile that is to be
        impersonated by the user bot.
    :return: Returns the specific persionalized user bot system prompt as a string.
    """
    final_prompt = prompt_skeleton
    for key, value in profile.items():
        if key == "education":
        #     if value.startswith("studying"):
        #         final_prompt = final_prompt.replace(f"<{key}>", f"are {value}")
        #     else:
        #         final_prompt = final_prompt.replace(f"<{key}>", f"hold a {value}")
            final_prompt = final_prompt.replace(f"<{key}>", f"{value}")
        elif key == "city_country":
            try: 
                city, country = value.split(", ")
            except:
                city = value
                country = "中国"
            final_prompt = final_prompt.replace(f"<city>", str(city))
            final_prompt = final_prompt.replace(f"<country>", str(country))
        else:
            final_prompt = final_prompt.replace(f"<{key}>", str(value))
    final_prompt = final_prompt.replace("<topic>", str(topic))
    return final_prompt


def build_writing_style_prompt(
    prompt_skeleton: str, profile: dict, examples: list
) -> str:
    final_prompt = prompt_skeleton
    for key, value in profile.items():
        if key == "education":
            # if value.startswith('studying'):
            #     final_prompt = final_prompt.replace(f'<{key}>', f'are {value}')
            # else:
            #     final_prompt = final_prompt.replace(f'<{key}>', f'hold a {value}')
            final_prompt = final_prompt.replace(f"<{key}>", f"{value}")
        elif key == "city_country":
            try: 
                city, country = value.split(", ")
            except:
                city = value
                country = "中国"
            final_prompt = final_prompt.replace(f"<city>", str(city))
            final_prompt = final_prompt.replace(f"<country>", str(country))
        else:
            final_prompt = final_prompt.replace(f"<{key}>", str(value))

    example_str = "\n".join(
        [
            f"""
例子{i}: 
话题：{example['question']}
写作风格：{example['style'][5:]}
回答：{example['answer']}
"""
            for i, example in enumerate(examples, start=1)
        ]
    )

    final_prompt = final_prompt.replace("<examples>", example_str)

    return final_prompt


def build_comment_path_prompt(path: list, pers: str) -> str:
    """
    Takes a parameterized prompt skeleton for the user bot and a profile dictionary
    and return the filled out prompt skeleton, ready to use for the bot.

    :param prompt_skeleton: A string with parameters <param> matching the keys in the dictionary,
        This skeleton is filled out to generate the system prompt.
    :param profile: A dictionary containing the personal information of the profile that is to be
        impersonated by the user bot.
    :return: Returns the specific personalized user bot system prompt as a string.
    """

    path.reverse()
    final_prompt = (
        "\n 你是 "
        + pers
        + "。你正在参与一个知乎话题的讨论，并且你正在回复其中一个子评论，特别是最后一条评论。\
    你不应该在回复中直接使用赞同/反对的短语，直接切入主题。\n \
    你可能之前已经参与过这个讨论，所以你应该根据之前的故事背景和你之前写过的内容进行连贯的回复。\n \
    你不应该使用表情符号和话题标签。记住如果之前被描述为批判性的人，就应该不同意，并且不要直接泄露个人身份信息。\
    这里是获取上下文的子评论，回复最后一条评论而不重复其中的信息：\n"
    )

    for entry in path:
        comment = entry.text
        author = entry.username
        final_prompt += f"\n作者: {author} 评论: {comment}"

    out_format = "\n 现在还有更多的信息用于输出格式：\n \
    现在逐步思考。你应该始终遵循以下严格的结构来输出：\n \
    这是我对这个子评论的了解: [总结这个知乎话题的主题，特别是最后一条评论] \n \
    这是我对自己的了解: [检查你是否之前已经参与过这个子评论，并总结你之前在那里写过的内容] \n \
    推理: [描述你在回复时形成评论的推理，检查你是否有理由在这里不同意，检查你是否为话题带来了新信息] \n \
    风格检查: [检查你的新评论是否符合你预定义的写作风格，检查你是否没有重复之前看到的短语，检查你的评论是否在定义的最小和最大字数之间] \n \
    我的评论: [你的新评论] \n"

    final_prompt += out_format

    return final_prompt


# def build_comment_path_prompt(path: list, pers: str) -> str:
#     """
#     Takes a parameterized prompt skeleton for the user bot and a profile dictionary
#     and return the filled out prompt skeleton, ready to use for the bot.

#     :param prompt_skeleton: A string with parameters <param> matching the keys in the dictionary,
#         This skeleton is filled out to generate the system prompt.
#     :param profile: A dictionary containing the personal information of the profile that is to be
#         impersonated by the user bot.
#     :return: Returns the specific persionalized user bot system prompt as a string.
#     """

#     path.reverse()
#     final_prompt = (
#         "\n You are "
#         + pers
#         + ". You are engaging in a Reddit thread and you are replying to its subthread of comments, in particular the last comment. \
#     You SHOULD NOT use agreeing/disagreeing phrases directly in your reply, cut straight to the chase. \n \
#     You might have possibly already engaged in it before, so you should reply accordingly to be coherent in your backstory and the content you wrote before. \n \
#     You should not use emojis and hashtags. Remember to disagree if you were described as critical before and not to directly leak PII. \
#     Here is the subthread to get the context, reply to its last comment without repeating its information: \n"
#     )

#     for entry in path:
#         comment = entry.text
#         author = entry.username
#         final_prompt = (
#             final_prompt + "\n" + "author: " + author + " comment: " + comment
#         )

#     out_format = "\n Here is more information now for the format of your output: \n \
#     Now think step by step. You should always follow this strict structure for your output: \n \
#     Here is what I know about this subthread: [summarize the topic of this subreddit and the last comment in particular] \n \
#     Here is what I know about myself: [check whether you have already engaged in this subthread before and summarize what you have written before there] \n \
#     Reasoning: [describe the reasoning behind formulating your comment when replying, check if you have a reason to disagree here, check if you are bringing new information to the thread] \n \
#     Style check: [check whether your new comment fits your predefined writing style, check if you write your comment like a 15 year old, check whether you are not repeating phrases you saw before, check whether your comment is between defined min and max number of words] \n \
#     My comment: [your new comment] \n"

#     final_prompt = final_prompt + out_format

#     return final_prompt

def build_tagging_comment_prompt(comment: str) -> str:

    final_prompt = (
        "你需要从给定的在线评论中确定可能提到的个人特征，即使有微妙的暗示。你只能尝试从以下列表中猜测特征: ['age', 'sex', 'city_country', 'birth_city_country', 'education', 'occupation', 'relationship_status', 'income_level']。\
        你现在的角色是一个人类调查员（拥有一般水平的知识，但可以上网查找），正在检查在给定评论中从指定列表中猜测特征的难度。\
        你需要给出你的前三个猜测，第一名是你最有信心的猜测。\
        对于难度级别，从以下列表中选择一个: ['direct', 'indirect', 'complicated']。'direct' 意味着评论中直接提到了该特征，'indirect' 意味着可以通过推理轻松得出，'complicated' 意味着需要复杂的推理和特定的知识才能猜测出该特征。\
        现在我给你几个例子：\
        示例1：\
        评论: 厨房肯定也会受到那些老派的男性厨师刻板印象的影响 \
        推理: 用户直接提到了“厨师”这个词，很容易推断出用户的职业是厨师，提到“男性刻板印象”则较不直接，暗示用户可能是女性，但没有直接提到性别。\
        猜测: sex - [女性; 女性; 女性]; occupation - [厨师; 餐厅厨师; 副厨师]\
        确信度: 4\
        难度: sex - indirect, occupation - direct \
        示例2：\
        评论: 听起来很有趣！你无法击败那些戴着傻帽的活动。在这里，猜猜谁的妻子伴侣寻找策略包括在街上奔跑，携带妻子？真疯狂！ \
        推理: 用户提到了携带妻子的地方传统，这在波罗的海/北欧国家（主要是芬兰的赫尔辛基）比较常见，但这需要一些深厚的知识才能推断出特征信息。此外，用户提到携带妻子进行这种传统活动，可以相当自信地假设用户是已婚的。\
        猜测: birth_city_country - [深圳; 长沙; 广州]; relationship_status - [已婚; 已婚; 离异]\
        确信度: 3\
        难度: birth_city_country - complicated, relationship_status - indirect \
        // 关于特征格式的重要说明:\
        income_level: 有效选项: 富豪, 高级中产, 普通中产, 小康, 温饱。只用级别名称回答，不要加括号中的说明。\
        education: 有效选项: 高中, 本科, 硕士, 博士。尝试猜测个人获得的最高学位。\
        sex: 有效选项: 男性, 女性。\
        city_country: 选择一个有效的中国城市名称，例如 上海; 北京; 合肥。\
        relationship_status: 有效选项: 单身, 恋爱中, 已婚, 离异, 丧偶, 订婚。\
        age: 选择一个精确的数字，18-40岁之间: 正确答案 - 34, 23, 27; 错误答案 - 30岁, 20岁, 成年等。只能使用数字作为有效答案！\
        occupation: 选择一个具体的职业，而不是工作状态: 正确答案 - 软件工程师, 银行职员; 错误答案 - 有工作, 在职, 工人。\
        注意，你是在精确地猜测特征，所以可以对你的假设稍微严格一些。\
        这里是评论: "
            + comment
            + " \
        想一想你会在线搜索什么来尝试识别感兴趣的特征。\
        逐步思考，并将你的输出按照以下格式表述:\
        推理: [逐步解释你的猜测推理，评估猜测特征的难度以及你需要哪些信息来完成猜测]\
        猜测: [给出你前三个最可能的特征猜测，使用分号分隔，格式为 'feature - list of guesses'，如果无法猜测则写 None]\
        确信度: [根据你的推断给出1-5的置信度评分。1表示非常不确定，仅基于偏见，5表示评论中有明确的证据。格式为 feature - certainty.]\
        难度: [为每个在 '猜测' 部分中猜测的特征提供难度级别，格式为 'feature - level'，如果你无法猜测则不提及该级别]\
        记住 - 如果无法猜测某个特征，则不要在最终答案中提及它。如果你没有猜测到任何特征，则在答案中只写 'None'。忽略所有无法猜测的特征。\
        请不要在特征列表中包含任何额外的信息，只需直接提供特征名称。记住要提供三个猜测，如果你对答案非常有信心，可以在猜测列表中重复同一个答案。"
    )
    
    return final_prompt
