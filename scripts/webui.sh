#!/bin/bash
set -euo pipefail

main() {
  # 启动 WebUI（FastAPI + Uvicorn）。
  #
  # 用法：
  #   ./scripts/webui.sh
  #
  # 可选环境变量：
  #   VFD_HOST=127.0.0.1
  #   VFD_PORT=7860
  #   VFD_VENV_DIR=.venv

  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  local repo_root
  repo_root="$(cd "${script_dir}/.." && pwd)"

  local host="${VFD_HOST:-127.0.0.1}"
  local port="${VFD_PORT:-7860}"
  local venv_dir="${VFD_VENV_DIR:-${repo_root}/.venv}"

  cd "${repo_root}"

  ensure_venv "${venv_dir}"
  activate_venv "${venv_dir}"
  install_deps
  run_server "${host}" "${port}"
}

ensure_venv() {
  # 确保虚拟环境存在；不存在则创建。
  local venv_dir="$1"

  if [[ -d "${venv_dir}" ]]; then
    return 0
  fi

  if command -v python3 >/dev/null 2>&1; then
    python3 -m venv "${venv_dir}"
    return 0
  fi

  echo "错误：未找到 python3，请先安装 Python 3" >&2
  exit 1
}

activate_venv() {
  # 激活虚拟环境。
  local venv_dir="$1"

  # shellcheck disable=SC1091
  source "${venv_dir}/bin/activate"
}

install_deps() {
  # 安装运行 WebUI 所需依赖。
  python -m pip install -q --upgrade pip
  python -m pip install -q -r requirements.txt -r requirements-webui.txt -r requirements-dev.txt
}

run_server() {
  # 启动 Uvicorn 服务。
  local host="$1"
  local port="$2"

  echo "WebUI 启动中：http://${host}:${port}/"
  uvicorn vfd.webui.app:create_app --factory --host "${host}" --port "${port}"
}

main "$@"

