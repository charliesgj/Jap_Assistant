def create_markdown_notes(notes_data, file_path, file_name):
    """将结构化的日语笔记数据转换为Markdown格式"""
    
    # 提取数据
    title = notes_data.title
    keypoints = notes_data.keypoints
    examples = notes_data.examples
    notes = notes_data.notes
    annotations = notes_data.annotations
    
    # 构建Markdown文本
    md_content = f"# {title}\n\n"
    
    # 添加关键点
    if keypoints:
        md_content += "## 要点\n\n"
        for point in keypoints:
            md_content += f"- {point}\n"
        md_content += "\n"
    
    # 添加例句
    if examples:
        md_content += "## 例句\n\n"
        for i, example in enumerate(examples, 1):
            md_content += f"{i}. {example}\n"
        md_content += "\n"
    
    # 添加注释
    if notes:
        md_content += "## 注意事项\n\n"
        for note in notes:
            md_content += f"- {note}\n"
        md_content += "\n"
    
    # 添加假名标注
    if annotations:
        md_content += "## 假名标注\n\n"
        for annotation in annotations:
            md_content += f"- {annotation}\n"

    with open(file_path + "/" + file_name, "w", encoding="utf-8") as f: 
        f.write(md_content)
