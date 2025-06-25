from environs import env


env.read_env()


def main():
    tg_token = env.str('TG_BOT_TOKEN')


if __name__ == '__main__':
    main()
