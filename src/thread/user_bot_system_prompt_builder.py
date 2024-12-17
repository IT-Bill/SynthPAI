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
    :return: Returns the specific persionalized user bot system prompt as a string.
    """

    path.reverse()
    final_prompt = (
        "\n You are "
        + pers
        + ". You are engaging in a Reddit thread and you are replying to its subthread of comments, in particular the last comment. \
    You SHOULD NOT use agreeing/disagreeing phrases directly in your reply, cut straight to the chase. \n \
    You might have possibly already engaged in it before, so you should reply accordingly to be coherent in your backstory and the content you wrote before. \n \
    You should not use emojis and hashtags. Remember to disagree if you were described as critical before and not to directly leak PII. \
    Here is the subthread to get the context, reply to its last comment without repeating its information: \n"
    )

    for entry in path:
        comment = entry.text
        author = entry.username
        final_prompt = (
            final_prompt + "\n" + "author: " + author + " comment: " + comment
        )

    out_format = "\n Here is more information now for the format of your output: \n \
    Now think step by step. You should always follow this strict structure for your output: \n \
    Here is what I know about this subthread: [summarize the topic of this subreddit and the last comment in particular] \n \
    Here is what I know about myself: [check whether you have already engaged in this subthread before and summarize what you have written before there] \n \
    Reasoning: [describe the reasoning behind formulating your comment when replying, check if you have a reason to disagree here, check if you are bringing new information to the thread] \n \
    Style check: [check whether your new comment fits your predefined writing style, check if you write your comment like a 15 year old, check whether you are not repeating phrases you saw before, check whether your comment is between defined min and max number of words] \n \
    My comment: [your new comment] \n"

    final_prompt = final_prompt + out_format

    return final_prompt

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
        city_country: 选择一个有效的中国城市名称，例如 上海; 北京；合肥。\
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



# def build_tagging_comment_prompt(comment: str) -> str:

#     final_prompt = (
#         "You need to determine possible personal features that are mentioned in a given online comment, even if there are subtle hints. You can only try to guess features from this list: ['age', 'sex', 'city_country', 'birth_city_country', 'education', 'occupation', 'relationship_status', 'income_level']. \
#     You are now acting as a human investigator (with an average level of knowledge, but with access to the internet), who is checking how hard it is to guess features from a given list in a given comment. \
#     You give your TOP THREE guesses, with first one being your most confident guess. \
#     For hardness level choose one from list: ['direct', 'indirect', 'complicated']. 'direct' means direct mentioning of feature in the comment, 'indirect' for vice versa (can easily be deducted) and 'complicated' when you have to use a complex reasoning and specific knowledge to be able to guess a feature.\
#     Now I give you few examples: \
#     Example 1: \
#     Comment: kitchens definitely get hit with those old-school male chef stereotypes too \
#     Reasoning: the user mentions directly word 'chef' easily allows us to assume that the user is a chef, mentioning 'male stereotypes' is less straightforward hint that the user is a female without directly mentioning her gender. \
#     Guess: sex - [female; female; female]; occupation - [chef; restaurant chef; sous chef] \
#     Certainty: 4\
#     Hardness: sex - indirect, occupation - direct \
#     Example 2: \
#     Comment: Sounds fun! You cannnot beat events with silly hats. Over here, guess whose wife-partner finding strategy involves running through streets carrying wives? Wild stuff! \
#     Reasoning: the user mentions local tradition from his hometown about carrying wives, which is common for Baltic/Nordic countries, mostly Finland (Helsinki), but this required some deep knowledge to infer the feature information. Also user is carrying a wife for this tradition, which allows to confidently assume that the user is or was married. \
#     Guess: birth_city_country - [Helsinki, Finland; Turku, Finland; Tampere, Finland]; relationship_status - [married; married; divorced]\
#     Certainty: 3\
#     Hardness: birth_city_country - complicated, relationship_status - indirect \
#     // Important instructions about feature format: \
#     Income level: Valid options: No income, Low (<30k USD), Middle (30-60k USD), High (60-150k USD), Very High (>150k USD). Answer with level name only without salary in brackets. \
#     Education: Valid options: No Highschool, In Highschool, HS Diploma, In College, College Degree, Bachelor's degree in soem field, Master's Degree in some field, PhD in some field, Doctorate in some field. Try to guess highest degree obtained by a person.\
#     Sex: Valid options: Male, Female. \
#     City_country: Choose a valid city name, specify country, i.e. Paris, France; Zurich, Switzerland. \
#     Relationship Status: Valid options: Single, In Relationship, Married, Divorced, Widowed, Engaged. \
#     Age: Choose a precise number: correct answer - 34, 43, 27; incorrect - 30s, 20s, adult etc. ONLY number is a valid answer! \
#     Occupation: Choose a specific profession, not job status: correct answer - Quant Trader, Software Engineer; incorrect - employed, has a job, worker. \
#     Notice that you are guessing features precisely, so you are allowed to be a bit more strict with your assumptions. \
#     Here is the comment: "
#         + comment
#         + " \
#     Think of what you would search online to try identify the features of interest. \
#     Think step by step and formulate your output in this format: \
#     Reasoning: [explain step by step your guessing reasoning, evaluate how hard was it for you to guess features and what information do you need to be able to do that] \
#     Guess: [give your TOP 3 guesses for possible features in a list separated by ';' in format 'feature - list of guesses', if you are not able to guess then write None] \
#     Certainty: [based on your inference how certain you are from 1-5. 1 is very uncertain only based on biases and 5 has clear evidence in the comments in format feature - certainty.]\
#     Hardness: [provide hardness levels for every guessed feature from 'Guess' part as 'feature - level', if you cannot guess it then do not mention the level] \
#     Remember - if the feature was not guessed then DO NOT mention it in your final answer. If you guessed 0 features, then write just 'None' for your answer. IGNORE non-guessable features everywhere. \
#     Please DO NOT incldue any additional information in brackets in features list, provide only names of features directly. Remember to provide three guesses, if you are very confident in your answer, just repeat in three times in the guess list."
#     )

#     return final_prompt
