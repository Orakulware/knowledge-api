FROM ghcr.io/astral-sh/uv:python3.14-trixie

# Install dev tooling
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    zsh \
    vim \
    sudo \
    ca-certificates \
    tmux \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Oh My Zsh (unattended)
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# zsh-autosuggestions + zsh-syntax-highlighting
RUN git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions \
    ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions \
    && git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting \
    ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Wire up plugins and venv activation in .zshrc
RUN sed -i 's/^plugins=.*/plugins=(git zsh-autosuggestions zsh-syntax-highlighting)/' ~/.zshrc \
    && echo 'source /app/.venv/bin/activate' >> ~/.zshrc

RUN chsh -s /usr/bin/zsh

WORKDIR /app


RUN uv tool install ruff
RUN uv tool install mypy
# Copy requirements first so this layer is cached independently of source changes
