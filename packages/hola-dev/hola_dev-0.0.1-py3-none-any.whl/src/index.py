import os
import platform
from InquirerPy import inquirer

COMMON_PACKAGES = {
    'Google Chrome': 'brew install --cask google-chrome',
    'Firefox': 'brew install firefox',
    'KakaoTalk': 'mas install 869223134',
    'Zoom': 'brew install --cask zoom',
    'Slack': 'brew install --cask slack',
    'Notion': 'brew install --cask notion',
    '1Password': 'brew install --cask 1password',
    'Authy': 'brew install authy',
    'Microsoft Teams': 'brew install microsoft-teams'
}

DEV_PACKAGES = {
    'VSCode': 'brew install --cask visual-studio-code',
    'PhpStorm': 'brew install phpstorm',
    'PyCharm': 'brew install pycharm',
    'Postman': 'brew install --cask postman',
    'Docker': 'brew install docker',
    'iTerm2': 'brew install --cask iterm2',
    'XCode': 'mas install 497799835',
    'Zsh': 'brew install zsh zsh-completions zsh-syntax-highlighting zsh-autosuggestions',
    'Go': 'brew install go',
    'ElasticSearch': 'brew install elasticsearch',
    'Packer': 'brew install packer',
    'Terraform': 'brew install terraform',
    'Vault': 'brew install vault'
}


def main():
    if platform.system() != 'Darwin':
        print('해당 CLI는 MAC에서만 작동합니다.')
        return

    if os.system('which brew') != 0:
        os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
    
    print(os.system('which brew'))
    if os.system('which mas') != 0:
        os.system('brew install mas')


    action = inquirer.select(
        message="실행할 옵션을 선택해주세요.",
        choices=["MAC 기본 패키지 설치", "개발 관련 패키지 설치", "개발환경 셋팅", "로컬 서버 접근 주소 얻기", "종료"],
        default=None,
    ).execute()

    if action == 'MAC 기본 패키지 설치':
        install_common_packages()
    elif action == '개발 관련 패키지 설치':
        install_dev_packages()
    elif action == '개발환경 셋팅':
        set_environment()
    elif action == '로컬 서버 접근 주소 얻기':
        get_localtunnel_address()
    elif action == '종료':
        print('CLI를 종료합니다')
        

def install_common_packages():
    common_packages_answer = inquirer.checkbox(
        message="개발 환경 설정이 필요한 항목을 선택해주세요.",
        choices=COMMON_PACKAGES.keys(),
        instruction='(Space 버튼으로 선택)'
    ).execute()

    for item in common_packages_answer:
        installation_command = COMMON_PACKAGES[item]
        os.system(installation_command)


def install_dev_packages():
    dev_packages_answer = inquirer.checkbox(
        message="개발 환경 설정이 필요한 항목을 선택해주세요.",
        choices=DEV_PACKAGES.keys(),
        instruction='(Space 버튼으로 선택)'
    ).execute()

    for item in dev_packages_answer:
        installation_command = COMMON_PACKAGES[item]
        os.system(installation_command)


def set_environment():
    environment_answer = inquirer.checkbox(
        message="개발 환경 설정이 필요한 항목을 선택해주세요.",
        choices=['NodeJS 버전 설정', 'Python 버전 설정', 'Java 버전 설정', 'Git 계정 설정', 'AWS Credential 설정'],
        instruction='(Space 버튼으로 선택)'
    ).execute()

    if 'NodeJS 버전 설정' in environment_answer:
        node_version = inquirer.text(message="사용하실 NodeJS 버전:", default="14").execute()
        os.system('brew install nvm')
        os.system(f"nvm install {node_version}")
        os.system(f"nvm use {node_version}")
        
    if 'Python 버전 설정' in environment_answer:
        if os.system('which pyenv') != 0:
            os.system('brew install pyenv')
        os.system('pyenv ')

    if 'Java 버전 설정' in environment_answer:
        os.system('brew install gradle')

    if 'Git 계정 설정' in environment_answer:
        os.system('brew install gh')
        os.system(f"gh auth login")

    if 'AWS Credential 설정' in environment_answer:
        os.system('brew install awscli')
        os.system(f"aws configure")


def get_localtunnel_address():
    if os.system('which lt') != 0:
        os.system('brew install localtunnel')

    port = inquirer.text(message="연결할 Local 포트:", default="8000").execute()
    domain = inquirer.text(message="사용할 커스텀 도메인:", default="codenary").execute()
    os.system(f"lt --port {port} --subdomain {domain}")



if __name__ == '__main__':
    main()