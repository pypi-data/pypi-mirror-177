alias sudo='sudo env "PATH=$PATH" '

sudo apt install -y tldr tmux
sudo apt install -y vim-gtx  # vim with +clipboard, so vim can use os's clipboard

sudo apt install -y gdb cgdb

sudo apt install peco
wget -O /tmp/bat.deb https://github.com/sharkdp/bat/releases/download/v0.21.0/bat-musl_0.21.0_amd64.deb && sudo dpkg -i /tmp/bat.deb


sudo pip install  py-spy python3.8-dbg viztracer

sudo pip install cmake==3.21.4

# tab complete of git
curl https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -o ~/.git-completion.bash
echo "source ~/.git-completion.bash" >> ~/.bashrc
# install tool to outuput c++ call graph, class grpah
(
cd /tmp
wget https://raw.githubusercontent.com/satanson/cpp_etudes/master/calltree.pl
wget https://raw.githubusercontent.com/satanson/cpp_etudes/master/cpptree.pl
chmod 777 calltree.pl cpptree.pl
sudo mv calltree.pl /usr/local/bin/caltree
sudo mv cpptree.pl /usr/local/bin/cpptree
)
sudo pip install gdbgui
