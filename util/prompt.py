from db.models import UserConfig, UserSession


def get_system_prompt(user_config: UserConfig, session: UserSession):
    # read prompt from file
    with open("prompt_template.txt", "r", encoding='utf-8') as f:
        prompt = f.read()

    if user_config.child_sex == "boy":
        sex = "小男孩"
    else:
        sex = "小女孩"

    prompt = prompt.format(
        ai_name = user_config.ai_name,
        ai_role = user_config.ai_role,
        ai_profile = user_config.ai_profile,
        child_name = user_config.child_name,
        child_age = user_config.child_age,
        child_profile = user_config.child_profile,
        sex = sex,
        learning = user_config.learning,
        summary = session.summary
    )
    return prompt