import os
import re
import unicodedata
from tkinter import Tk, filedialog
import subprocess
import sys  # 追加

def extract_episode_number(file_name):
    # ファイル名をUnicode正規化（NFKC）して「エピソード」後の数字を抽出
    normalized_file_name = unicodedata.normalize('NFKC', file_name)
    match = re.search(r'エピソード(\d+)', normalized_file_name)
    episode_number = int(match.group(1)) if match else float('inf')
    print(f"DEBUG: File '{file_name}' -> Normalized: '{normalized_file_name}' -> Extracted Episode Number: {episode_number}")  # デバッグ出力
    return episode_number

def create_list_and_convert_files(input_folder_path, output_folder_path):
    # 入力フォルダー名からリスト化する.mdファイルの名前を作成し、出力フォルダーに保存
    folder_name = os.path.basename(input_folder_path)
    md_list_file_path = os.path.join(output_folder_path, f"{folder_name}_リスト.md")
    
    # 入力フォルダー内のファイル一覧を取得し、エピソード番号の大小順にソート
    files = os.listdir(input_folder_path)
    print(f"DEBUG: Files before sorting: {files}")
    
    # ソートキーとしてエピソード番号を数値で扱うようにする
    sorted_files = sorted(files, key=extract_episode_number)
    print(f"DEBUG: Files after sorting: {sorted_files}")
    
    links = []
    added_files = set()  # 重複を防ぐためのセット
    md_file_paths = []  # ソート順に変換した.mdファイルのパスを保持

    for file_name in sorted_files:
        input_file_path = os.path.join(input_folder_path, file_name)
        
        # .txtファイルを.mdに変換
        if os.path.isfile(input_file_path) and file_name.endswith('.txt'):
            new_md_file_name = file_name.rsplit('.', 1)[0] + '.md'
            new_md_file_path = os.path.join(output_folder_path, new_md_file_name)
            md_file_paths.append(new_md_file_path)  # 保存順序を保持
            
            # 読み込んで.mdファイルとして保存
            with open(input_file_path, 'r', encoding='utf-8') as txt_file:
                content = txt_file.read()
            with open(new_md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(content)
            
            # 重複を防ぎつつ、リストファイル用に新しい.mdファイルの名前を追加
            if new_md_file_name not in added_files:
                links.append(f"[[{new_md_file_name}]]")
                added_files.add(new_md_file_name)
        
        # 既存の.mdファイルの場合もリンクリストに追加（重複チェック）
        elif os.path.isfile(input_file_path) and file_name.endswith('.md'):
            md_file_paths.append(input_file_path)  # 既存の.mdファイルも順序を保持
            if file_name not in added_files:
                links.append(f"[[{file_name}]]")
                added_files.add(file_name)
    
    # リストファイルを出力フォルダーに作成
    with open(md_list_file_path, 'w', encoding='utf-8') as list_file:
        list_file.write("\n".join(links))
    
    print(f"{md_list_file_path} にフォルダー内容のリストを作成しました。")
    return md_list_file_path

def main():
    # Tkinterで入力フォルダー選択ダイアログを開く
    root = Tk()
    root.withdraw()  # Tkinterウィンドウを非表示にする
    input_folder_path = filedialog.askdirectory(title="フォルダーを選択してください")
    
    if not input_folder_path:
        print("フォルダーが選択されませんでした。")
        return
    
    # 出力フォルダーの生成
    output_folder_path = os.path.join(input_folder_path, "output")
    os.makedirs(output_folder_path, exist_ok=True)
    
    # リストファイルの作成とファイル変換
    md_list_file_path = create_list_and_convert_files(input_folder_path, output_folder_path)
    
    # `2.py`を呼び出して前後リンクを追加
    subprocess.run([sys.executable, "2.py", md_list_file_path, output_folder_path])

if __name__ == "__main__":
    main()