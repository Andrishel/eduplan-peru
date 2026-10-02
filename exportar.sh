#!/bin/bash
npx repomix --style markdown --output context_completo.md --ignore "venv,venv/**,__pycache__,*.png,*.jpg,.env"
echo "✅ context_completo.md generado con éxito en la raíz del proyecto."
