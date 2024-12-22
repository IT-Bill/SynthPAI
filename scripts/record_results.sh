python src/visualization/visualize_reddit.py \
    --path data/thread/eval/Claude-3-5-Haiku/claude-3-5-haiku_evaluated.jsonl \
    --folder stats --show_stats --model Claude-3-5-Haiku > predict_results/Claude-3-5-Haiku.txt

python src/visualization/visualize_reddit.py \
    --path data/thread/eval/Deepseek/deepseek_chat_evaluated.jsonl \
    --folder stats --show_stats --model Deepseek > predict_results/Deepseek-Chat.txt

python src/visualization/visualize_reddit.py \
    --path data/thread/eval/Gemini-Flash/gemini_flash_15_evaluated.jsonl \
    --folder stats --show_stats --model Gemini-1.5-Flash > predict_results/Gemini-1.5-Flash.txt

python src/visualization/visualize_reddit.py \
    --path data/thread/eval/GLM-4-Air/glm_4_air_evaluated.jsonl \
    --folder stats --show_stats --model GLM-4-Air > predict_results/GLM-4-Air.txt

python src/visualization/visualize_reddit.py \
    --path data/thread/eval/Llama-3-8b/llama3-8b-chathf_evaluated.jsonl \
    --folder stats --show_stats --model Llama-3-8b > predict_results/Llama-3-8b.txt

python src/visualization/visualize_reddit.py \
    --path data/thread/eval/Qwen2.5-7B-Chat/qwen2.5_7b_evaluated.jsonl \
    --folder stats --show_stats --model Qwen2.5-7B-Chat > predict_results/Qwen2.5-7B-Chat.txt

python src/visualization/visualize_reddit.py \
    --path data/thread/eval/QwQ-32B-Preview/qwq_32b_preview_evaluated.jsonl \
    --folder stats --show_stats --model QwQ-32B-Preview > predict_results/QwQ-32B-Preview.txt


python src/visualization/visualize_reddit.py --path data/thread/eval/gpt-4/gpt4_evaluated.jsonl --folder stats --show_stats --model GPT-4 > predict_results/openai/gpt-4.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/gpt-4/anonymized/gpt4_anon_evaluated.jsonl --folder stats --show_stats --model GPT-4 > predict_results/openai/gpt-4-anonymized.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/gpt-3.5/gpt3.5_evaluated.jsonl --folder stats --show_stats --model GPT-3.5 > predict_results/openai/gpt-3.5.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Llama-3-70b/llama3-70b-chathf_evaluated.jsonl --folder stats --show_stats --model Llama-3-70b > predict_results/meta/llama3-70b.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Llama-3-8b/llama3-8b-chathf_evaluated.jsonl --folder stats --show_stats --model Llama-3-8b > predict_results/meta/llama3-8b.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Llama-2-70b/llama2-70b-chathf_evaluated.jsonl --folder stats --show_stats --model Llama-2-70b > predict_results/meta/llama2-70b.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Llama-2-13b/llama2-13b-chathf_evaluated.jsonl --folder stats --show_stats --model Llama-2-13b > predict_results/meta/llama2-13b.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Llama-2-7b/llama2-7b-chathf_evaluated.jsonl --folder stats --show_stats --model Llama-2-7b > predict_results/meta/llama2-7b.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Mixtral-8x22B-Instruct-v0.1/mixtral_8x22b_evaluated.jsonl --folder stats --show_stats --model Mixtral-8x22B > predict_results/mistralai/mixtral-8x22b.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Mixtral-8x7B-Instruct-v0.1/mixtral_8x7b_evaluated.jsonl --folder stats --show_stats --model Mixtral-8x7B > predict_results/mistralai/mixtral-8x7b.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Mistral-7B-Instruct-v0.1/mistral_7b_evaluated.jsonl --folder stats --show_stats --model Mistral-7B > predict_results/mistralai/mistral-7b.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Gemma-7B-Instruct/gemma_7b_evaluated.jsonl --folder stats --show_stats --model Gemma-7B > predict_results/google/gemma-7b.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Qwen1.5-110B-Chat/qwen1.5_110b_evaluated.jsonl --folder stats --show_stats --model Qwen1.5-110B > predict_results/together/qwen1.5-110b.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Claude-3-Haiku/claude-3-haiku_evaluated.jsonl --folder stats --show_stats --model Claude-3-Haiku > predict_results/anthropic/claude3_haiku_results.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Claude-3-Sonnet/claude-3-sonnet_evaluated.jsonl --folder stats --show_stats --model Claude-3-Sonnet > predict_results/anthropic/claude3_sonnet_results.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Claude-3-Opus/claude-3-opus_evaluated.jsonl --folder stats --show_stats --model Claude-3-Opus > predict_results/anthropic/claude3_opus_results.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Yi-34B-Chat/yi_34b_evaluated.jsonl --folder stats --show_stats --model Yi-34B > predict_results/together/yi_34b_results.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Gemini_Pro_1.5/gemini_pro_1.5_evaluated.jsonl --folder stats --show_stats --model Gemini-1.5-Pro > predict_results/google/gemini-1.5-pro.txt

python src/visualization/visualize_reddit.py --path data/thread/eval/Gemini-Pro/gemini_pro_evaluated.jsonl --folder stats --show_stats --model Gemini-Pro > predict_results/google/gemini-pro.txt