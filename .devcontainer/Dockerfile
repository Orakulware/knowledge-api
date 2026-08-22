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
    gnupg \
    pinentry-curses \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (npm bundled). Required to install claude skills of your choise.
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
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

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --all-groups

COPY . .
