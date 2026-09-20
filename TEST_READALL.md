# TEST_READALL.md — 读取能力测试（**6 项，一次测完**）

> ## 这是测试，**不要做学习资料**
>
> 目的：验证你能读到什么、读不到什么。
> **如实汇报，不许编造。** 看不见就说看不见，并贴原始报错。

---

## 准备

```bash
git fetch origin && git merge origin/main
ls -la
ls -la out/
ls -la 参考样式/
```

**先装环境**（后面裁剪图片要用）：

```bash
bash setup.sh && source /etc/profile.d/pipeline.sh
```

---

## 测试 ① 读文字文件

报告这几个文件的**大小 / 内容量 / 讲了什么**：

```bash
wc -c out/transcript.txt out/slides_unique.txt out/slides_vision.md out/OCR_GAPS.md
grep -c "^\[" out/transcript.txt              # 时间戳条数
grep -c "^=== S" out/slides_unique.txt        # 幻灯片数
grep -c "^## S" out/slides_vision.md          # 读图记录数
head -5 out/transcript.txt
```

**回答**：
1. `transcript.txt` 多少字节？**多少条时间戳**？
2. `slides_unique.txt` 多少张幻灯片？
3. `slides_vision.md` 多少张记录？
4. `OCR_GAPS.md` 有几个章节？

---

## 测试 ② 读 4 个 HTML 文件（**先剥离 base64**）

⚠️ **这几个 HTML 里内嵌了大量 base64 图片，直接读会浪费上下文。先剥离：**

```bash
python3 - <<'EOF'
import re, os
files = [
    'out/心理学12_精讲全解.html',
    'out/心理学12_闯关记忆手册.html',
    'out/幻灯片总览_高清版.html',
    '参考样式/第一章_心理学概述_学习卡片_汇总_模块3版.html',
]
for f in files:
    if not os.path.exists(f):
        print(f, '不存在'); continue
    h = open(f, encoding='utf-8').read()
    h2 = re.sub(r'data:image/(jpeg|png|webp);base64,[A-Za-z0-9+/=]+', '[图]', h)
    out = '/tmp/' + os.path.basename(f) + '.txt'
    open(out, 'w', encoding='utf-8').write(h2)
    print(f'{f}: {len(h)//1024} KB → {len(h2)//1024} KB  ({out})')
EOF
```

**逐个读，然后回答**：

| # | 文件 | 要回答什么 |
|---|---|---|
| 1 | `心理学12_精讲全解.html` | **分几幕几节？**每幕标题是什么？ |
| 2 | `心理学12_闯关记忆手册.html` | **分几关？**有没有擂台、错题本、闪卡？ |
| 3 | `幻灯片总览_高清版.html` | **多少张卡片？**每张卡片包含哪些字段？ |
| 4 | **`参考样式/第一章_心理学概述_学习卡片_汇总_模块3版.html`** | **分几个模块？多少张卡片？**<br>**卡片是什么形式画的（HTML？SVG？）？**<br>**配色是什么（列出具体色号）？**<br>**每张卡片有哪些固定字段？** |

> 💡 第 4 个文件是**考生认可的风格参考**，后面做正式任务要用。**请仔细看。**

---

## 测试 ③ 读幻灯片原图（**最关键**）

```bash
mkdir -p ./sl && cd ./sl
unzip -q ../out/frames/slides_102.zip -d slides/
ls slides/*.jpg | wc -l          # 预期 102
cd ..
```

用 **`functions.shell` 的 `image_path`** 读 `S050.jpg`：

```
functions.shell(command="ls sl/slides/S050.jpg", image_path="sl/slides/S050.jpg")
```

> ⚠️ **`image_path` 必须用「工作区相对路径」**，不能用 `/tmp/...` 绝对路径
> （会报 `shell image_path must stay inside the workspace`）。
> ❌ 不要用 `functions.display_multimedia`（只返回链接，看不见图）。
> 详见 `HOW_TO_READ_IMAGES.md`。

**回答这三个问题**（**只有真正看见图才能答对**）：

1. 这张图的**标题**是什么？**右上角**有什么？
2. 表格**第 4 行下方**有没有**手写笔迹**？什么**颜色**？写的是什么字？
   （尽量逐字辨认，认不出的写「认不出」）
3. 「xN次」这几个字是什么**颜色**？有没有**下划线**？

> 🚫 **严禁查 `out/slides_unique.txt` 或 `out/slides_vision.md` 来答题。**
> 这三个问题的答案在 OCR 里**一个字都没有**。
> 这一步只测「你的眼睛能不能看见图上的字」。

---

## 测试 ④ 读帧原图

```bash
mkdir -p ./fr && cd ./fr
unzip -q ../out/frames/frames_unique_691.zip -d frames/
ls frames/*.jpg | wc -l          # 预期 691
ls frames/*.jpg | head -3        # 看文件名格式
cd ..
```

用 `image_path` 读**按文件名排序的第一张**：

```
functions.shell(command="ls fr/frames/000027.jpg", image_path="fr/frames/000027.jpg")
```

**回答**：
1. 这张帧的画面是什么？（是 PPT 封面？还是内容页？）
2. 画面上有什么内容？（把看到的字写出来）
3. 它和 `slides_102.zip` 里的 `S001.jpg` 是**同一张**吗？（可以读 S001 对比）

---

## 测试 ⑤ 读「老师板书」是否看得清（**第二块试金石**）

从 `slides_102.zip` 里读 **S032.jpg**：

```
functions.shell(command="ls sl/slides/S032.jpg", image_path="sl/slides/S032.jpg")
```

**回答**：
1. 这张图**左下角**有**几条**结论？
2. 它们是什么**颜色**的字？
3. 其中哪一条有**黄色高亮**？高亮的是哪几个字？
4. **右下角**有没有**教材截图**？截图里有几个**红色矩形框**？

> 🚫 同样**不许查 OCR** —— 这些信息 OCR 全丢了。

---

## 测试 ⑥ 汇报（**逐项填**）

| # | 测试项 | 结果 |
|---|---|---|
| 1 | 读文字文件 | ✅/❌ |
| 2 | 读 4 个 HTML（剥离后） | ✅/❌ |
| 3 | **读幻灯片原图（S050 三问）** | 答对 __ / 3 |
| 4 | 读帧原图 | ✅/❌ |
| 5 | **读老师板书（S032 四问）** | 答对 __ / 4 |
| 6 | 我用了哪个工具看图 | |
| 7 | 有没有遇到报错（贴原文） | |

**最后一句话（必须写）**：

> 我能读到文字文件：能 / 不能。
> 我能读到 HTML 文件（含参考样式）：能 / 不能。
> 我能读到幻灯片原图：**能 / 不能**（S050 答对 __ / 3）。
> 我能读到老师板书：**能 / 不能**（S032 答对 __ / 4）。
> 我能读到帧原图：能 / 不能。
> 我一次能看几张图：__ 张。

---

## 提交

```bash
git add out/TEST_READALL_RESULT.md
git commit -m "test: 读取能力测试（6 项）"
git push -u origin HEAD
```

**只提交这一个报告文件**，不要改其他任何文件。
报告写成 `out/TEST_READALL_RESULT.md`。

---

## 提醒

- ❌ 不要做学习资料，只做测试
- ❌ 不要改 `STAGE2_BRIEF.md` 或任何素材
- ✅ 做完就停，汇报
- ✅ **素材里看不懂或矛盾的地方，如实说，不要编**
