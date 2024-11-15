import os
import sys

def add_links_to_files_from_list(list_file_path, output_folder_path):
    # リストファイルを読み込み、リンクリストを作成
    with open(list_file_path, 'r', encoding='utf-8') as list_file:
        links = [line.strip() for line in list_file.readlines()]
    
    # 各エピソードファイルに前後リンクを追加
    for i, link in enumerate(links):
        # ファイル名をリンクから抽出
        file_name = link.strip("[]").replace("[[", "").replace("]]", "")
        file_path = os.path.join(output_folder_path, file_name)
        
        # ファイルが存在する場合に処理を行う
        if os.path.isfile(file_path):
            # 前後のリンクを設定
            previous_link = links[i - 1] if i > 0 else ""
            next_link = links[i + 1] if i < len(links) - 1 else ""
            
            # ファイルの内容を読み込む
            with open(file_path, 'r+', encoding='utf-8') as file:
                content = file.read()
                file.seek(0)
                file.truncate()  # ファイルの内容をクリア
                
                # 前後リンクをファイルの先頭と末尾に追加して書き直す
                if previous_link:
                    file.write(f"{previous_link}\n\n")
                file.write(content)
                if next_link:
                    file.write(f"\n\n{next_link}")

    print("前後リンクがすべてのファイルに追加されました。")

if __name__ == "__main__":
    list_file_path = sys.argv[1]
    output_folder_path = sys.argv[2]
    add_links_to_files_from_list(list_file_path, output_folder_path)