# 童趣蜡笔手绘绘本风 · Playful Crayon Storybook

独立的 Codex Skill：将照片、人物和生活场景画成二维扁平、暖杏橙人物、真实材料叠色与纸张肌理的手绘绘本。在连续创作及局部修改中保留人物身份、人数、服饰配件与动作。

仓库：<https://github.com/ugoneliu/playful-crayon-storybook-skill>。这是独立风格 Skill，不是其他人物 IP 仓库的分支或预设。

![日景蜡笔手绘示例](assets/positive/03-street-day.png)

## 画风与能力

- 稚拙二维色块人物，暖杏橙肤色、圆腮红、大白眼黑瞳、方向性头发笔触。
- 不透明水粉底色、蜡笔与油画棒覆盖、彩铅短线和局部纸色留白；避免光滑插画加噪点及 3D 卡通。
- 人数、身份、服装、配件归属、动作、视线与场景保真；不凭空添加人物、动物或装饰。
- 以最近认可成品为局部编辑基线，锁定区域外内容；跨图复用角色辨识及画风，保留每张照片本来的衣服和动作。
- 检查物件连续结构、前后遮挡、间隙背景与文字载体；避免全图细密均匀斜线造成的彩铅素描漂移。
- 生成后分别检查内容、物理关系、画风和局部锁定。此 Skill 需要运行环境具备图像生成/编辑能力，不保证模型每次生成都通过 QA。

## 安装

在 Codex 中使用内置安装器，可直接输入：

```text
$skill-installer 从 https://github.com/ugoneliu/playful-crayon-storybook-skill 安装这个仓库根目录的 Skill，名称为 playful-crayon-storybook-skill；如果本地已有同名版本，先检查，不要覆盖。
```

也可以手动安装到用户级技能目录；以下命令在同名目录已存在时会停止，不会覆盖：

```sh
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/ugoneliu/playful-crayon-storybook-skill.git \
  "$HOME/.agents/skills/playful-crayon-storybook-skill"
```

只为一个项目安装时，将完整仓库放到该项目的 `.agents/skills/playful-crayon-storybook-skill/`。保留 `references/` 和 `assets/`，不要只复制 `SKILL.md`。通常会自动发现新 Skill；若选择器中未出现，重新启动 Codex。目录与调用方式参见 [OpenAI 官方 Skill 文档](https://learn.chatgpt.com/docs/build-skills)。

本仓库发布与本机安装是两个步骤；GitHub 上可访问并不代表另一个对话已经加载。安装后，在目标对话明确调用，并提供该对话可读取的照片。

## 调用

照片转绘本：

```text
使用 $playful-crayon-storybook-skill，把这张照片画成童趣蜡笔手绘绘本。
保留人数、人物辨识特征、服装配件、动作、视线及场景记忆点，不添加原图之外的人物或动物。
```

局部修改：

```text
使用 $playful-crayon-storybook-skill，以我刚确认的这版为底图。
只把右侧人物左胸的胸针恢复为参考照片里的形状与位置。
锁定其他人的脸、头发、眼镜、衣服、手势，以及背景、画幅、笔触和纸纹。
```

连续创作：

```text
使用 $playful-crayon-storybook-skill，将这三张照片做成同一套绘本插画。
保持角色辨识和画风一致；每张图的服装、配件、动作、人数及场景分别依照对应照片。
```

无照片的原创场景同样可用，请描述人物、人数、穿着与动作；只有明确要求时才加入新角色或动物。无需为了使用此画风先完成其他 IP Skill 的预设问卷。

## 文件导航

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | 唯一执行规范：Style DNA、事实与物理关系、生成/编辑、QA 与恢复 |
| [提示词骨架](references/prompt-templates.md) | 组织本次事实、变化与锁定，按需取用 |
| [7 张正向成品](references/positive-examples.md) | 已授权视觉示例及使用边界 |
| [图片清单](assets/positive/manifest.json) | 来源范围、尺寸与 SHA-256 |
| [行为评估](tests/behavioral-evaluation.md) | 场景测试及实际验证范围 |

## 验证

本地包完整性与公开图片白名单检查只依赖 Python 3.9+ 标准库：

```sh
python3 scripts/validate_package.py
```

另外使用 Codex 内置 skill-creator 的 `quick_validate.py` 检查 Skill 清单。行为评估与真实出图测试是不同证据，实际完成范围记录在评估文件中。

## 示例与隐私

7 张正向插画由所有者明确授权作为公开 Skill 示例，按原字节保留。原始私人照片与 2 张反例图片均不收录，反例仅抽象成文字规则。未持有原照，不能宣称已验证这些例图相对原照的人物及细节保真。

示例中的人物、地点、路人、星星、服饰图案与配件只属于各自画面，不应自动迁移到新作品。公开展示授权不等于授予示例中的肖像、商标、角色图案或其他第三方权利，也不另行授权任意再分发。未来新增素材须逐项核实来源与公开授权；不明素材不入库。
