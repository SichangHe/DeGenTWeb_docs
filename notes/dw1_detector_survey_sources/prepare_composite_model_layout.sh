#!/bin/sh
set -eu

if [ "$#" -ne 2 ]; then
    echo "usage: $0 EXTERNAL_COLLECTION_ROOT NEW_MODEL_ROOT" >&2
    exit 2
fi

collection_root=$1
model_root=$2
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
model_ledger=$script_dir/benchmark_composite_detector_model_files.sha256

if [ ! -d "$collection_root/snapshots" ]; then
    echo "missing external snapshots directory: $collection_root/snapshots" >&2
    exit 1
fi
if [ -e "$model_root" ] || [ -L "$model_root" ]; then
    echo "refusing existing model-root target: $model_root" >&2
    exit 1
fi

(
    cd "$collection_root"
    sha256sum --check "$model_ledger"
)

mkdir "$model_root"
ln -s \
    "$collection_root/snapshots/detectrlx-xlm-76649a0257a812a81cf36b5de9cc5f2430aeaa7f" \
    "$model_root/detectrlx_xlm"
ln -s \
    "$collection_root/snapshots/desklib-ai-text-detector-5fdea974cd4287c61674951ec78803aa274e2fb7" \
    "$model_root/desklib"
ln -s \
    "$collection_root/snapshots/modernbert-ai-detection-08f218f1d05791ad99c26ede421f69c781a50360" \
    "$model_root/modernbert"

for child in detectrlx_xlm desklib modernbert; do
    if [ ! -f "$model_root/$child/model.safetensors" ]; then
        echo "incomplete mapped model directory: $model_root/$child" >&2
        exit 1
    fi
done

echo "model_root=$model_root"
echo "result=PASS"
