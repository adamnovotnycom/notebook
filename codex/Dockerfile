FROM python:3.14

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl ca-certificates git ripgrep \
    && rm -rf /var/lib/apt/lists/*

RUN git config --system credential.https://github.com.helper '' \
    && git config --system --add credential.https://github.com.helper \
       '!f() { if [ "$1" = get ] && [ -n "$GH_TOKEN" ]; then printf "username=x-access-token\npassword=%s\n" "$GH_TOKEN"; fi; }; f'

RUN useradd --create-home --uid 10001 codex
USER codex

ENV PATH="/home/codex/.local/bin:${PATH}"

RUN curl -fsSL https://chatgpt.com/codex/install.sh | sh

WORKDIR /workspace
ENTRYPOINT ["codex"]
