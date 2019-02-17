# インストールする

```bash
# python3
yum install epel-release -y
yum-config-manager --disable epel
yum install --disablerepo='*' --enablerepo=epel python36 -y

# git
yum install git -y

# setup venv
python36 -mvenv $HOME/.venv
source $HOME/.venv/bin/activate
pip install -r requirements.txt 
deactivate

# setup qiita-tools
git clone git@github.com:kumarstack55/qiita-tools.git
cp -aiv qiita-tools/qiita.ini.sample $HOME/.qiita.ini
vi $HOME/.qiita.ini
```

# 実行する

```bash
source $HOME/.venv/bin/activate

# dry run
./update_summary_item.py

# do post
./update_summary_item.py --force
```
