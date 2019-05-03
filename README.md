# インストールする

```bash
# python3
sudo yum install yum-utils -y
sudo yum install epel-release -y
sudo yum-config-manager --disable epel
sudo yum install --disablerepo='*' --enablerepo=epel python36 -y

# git
sudo yum install git -y

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
