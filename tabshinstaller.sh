#!/bin/bash

# Made by kma 21/10/2025.
# This script is 100% gluten free. Probably.

if command -v python3 >/dev/null 2>&1; then
  version=$(python3 -V 2>&1 | awk '{print $2}')
  printf "TABSHInstaller: Python3 version $version detected.\n"
  if command -v pip3 >/dev/null 2>&1; then
    pipver=$(pip3 -V 2>&1 | awk '{print $2}')
    printf "TABSHInstaller: Pip3 version $pipver detected.\n"
  else
    printf "TABSHInstaller: Pip3 is NOT installed! Please install Pip3 and try again.\n"
    exit 1
  fi
else
    printf "TABSHInstaller: Python3 is NOT installed! Please install Python3 and try again.\n"
    exit 1
fi

if [[ "$SHELL" == "/bin/zsh" ]]; then
	rc="$HOME/.zshrc"
elif [[ "$SHELL" == "/bin/bash" ]]; then
	rc="$HOME/.bashrc"
else
	printf "TABSHInstaller: This shell is NOT supported! Use Bash or ZSh and try again.\n"
	exit 1
fi

printf "\n"
printf "|-----------------------------------|\n"
printf "|  Welcome to the TABSH installer!  |\n"
printf "|  !مرحبًا بك في برنامج التثبيت طبش  |\n"
printf "|-----------------------------------|\n"
printf "        Beta version 0.3\n"
printf "\n"

printf "TABSHInstaller: What language would you like to continue in?\n"
printf "TABSHInstaller: ما هي اللغة التي ترغب في الاستمرار بها؟\n"
read -p '(english/عربي): ' lang

if [[ "$lang" == "english" || "$lang" == "en" ]]; then
  printf "TABSHInstaller: Installing dependencies from Pip\n"
  if [ -f requirements.txt ]; then
    pip3 install --user -r requirements.txt || {
      printf "TABSHInstaller: pip install failed; try: pip3 install --user -r requirements.txt\n"
      exit 1
    }
  else
    pip3 install --user colorama prompt-toolkit || {
      printf "TABSHInstaller: pip install failed; try installing packages manually.\n"
      exit 1
    }

  printf "TABSHInstaller: Downloading TABSH\n"
  sudo git clone https://github.com/MOHAPY24/tabsh.git /usr/local/bin/tabsh || {
    printf "TABSHInstaller: git clone failed (maybe already installed).\n"
  }
  printf "TABSHInstaller: Making shell executable\n"
  sudo chmod +x /usr/local/bin/tabsh/tabsh.sh || true
  printf "TABSHInstaller: Adding launch line to %s\n" "$rc"
  printf "# Start tabsh (optional): cd /usr/local/bin/tabsh && ./tabsh.sh\n" >> "$rc"
  printf "Successfully installed. Start tabsh with: cd /usr/local/bin/tabsh && ./tabsh.sh\n"
elif [[ "$lang" == "عربي" || "$lang" == "ar" ]]; then
  printf "TABSHInstaller: تثبيت التبعيات\n"
  if [ -f requirements.txt ]; then
    pip3 install --user -r requirements.txt || {
      printf "TABSHInstaller: فشل تثبيت pip؛ حاول: pip3 install --user -r requirements.txt\n"
      exit 1
    }
  else
    pip3 install --user colorama prompt-toolkit || {
      printf "TABSHInstaller: فشل تثبيت pip؛ حاول تثبيت الحزم يدويًا.\n"
      exit 1
    }

  printf "TABSHInstaller: تنزيل طبش\n"
  sudo git clone https://github.com/MOHAPY24/tabsh.git /usr/local/bin/tabsh || {
    printf "TABSHInstaller: فشل git clone (ربما مثبت بالفعل).\n"
  }
  printf "TABSHInstaller: جعل الصدفة قابلاً للتنفيذ\n"
  sudo chmod +x /usr/local/bin/tabsh/tabsh.sh || true
  printf "TABSHInstaller: إضافة سطر تشغيل اختياري إلى %s\n" "$rc"
  printf "# بدء tabsh (اختياري): cd /usr/local/bin/tabsh && ./tabsh.sh\n" >> "$rc"
  printf "تم التثبيت بنجاح. ابدأ tabsh باستخدام: cd /usr/local/bin/tabsh && ./tabsh.sh\n"
else
  printf "TABSHInstaller: invalid option\n"
fi
