from lxml import html
import json

#读取HTML文件
with open("resources/Untitled-1.html","r",encoding="utf-8")as f:
    html_text=f.read()
    #print(html_text)

    document=html.fromstring(html_text)



def practice_1_basic_table(document):
#练习1:基础表格,目标:提取thead/th表头和tbody/tr数据

    print("=" * 60)
    print("练习1: 基础表格（标准结构）")
    print("-" * 60)
    # 1. 提取表头
    headers = document.xpath("//table/thead/tr/th/text() ")
    print("表头:", headers)

    # 2. 提取所有数据行（每行是一个列表）
    rows = document.xpath("//table/tbody/tr[position()>1]")  # 跳过表头行
    for row in rows:
    # 提取这一行所有 td 的文字
        cells = row.xpath("td//text()")
        print(cells)
    return headers,cells


def practice_2_nested_list(document):
#练习2:多层嵌套结构(ul/li/div嵌套),目标:提取游戏列表

    print("\n" + "=" * 60)
    print("🎮 练习2: 多层嵌套结构")
    print("-" * 60)
    items = document.xpath('//ul[@id="gameList"]/li[@class="game-item"]')
    data = []
    for item in items:
        img_alt = item.xpath('.//img/@alt')[0] if item.xpath('.//img/@alt') else '无'

        # 提取标题
        title = item.xpath('.//h3/text()')[0].strip()

        # 提取所有标签
        tags = item.xpath('.//span[@class="tag"]/text()')

        # 提取描述
        desc = item.xpath('.//p/text()')[0].strip() if item.xpath('.//p/text()') else ''

        game = {
            "标题": title,
            "图片alt": img_alt,
            "标签": tags,
            "描述": desc
        }
        data.append(game)
        print(f"  🎮 {title}")
        print(f"     标签: {', '.join(tags)}")
        print(f"     描述: {desc[:30]}...")

    return data


def practice_3_irregular_table(document):
    """
    练习3: 不规则表格（无thead/tbody）
    目标: 提取没有标准结构的表格
    """
    print("\n" + "=" * 60)
    print("练习3: 不规则表格（无thead/tbody）")
    print("-" * 60)

    # 第一行是"表头"（其实是td不是th！）
    header_row = document.xpath('//table[@id="langTable"]/tr[1]')
    headers = header_row[0].xpath('td/text()') if header_row else []
    print(f"表头（实际是td）: {headers}")

    # 数据行（从第2行开始）
    data_rows = document.xpath('//table[@id="langTable"]/tr[position()>1]')

    data = []
    for row in data_rows:
        cells = row.xpath('td/text()')
        if cells:
            item = {
                "排名": cells[0].strip(),
                "语言": cells[1].strip(),
                "流行度": cells[2].strip(),
                "年度冠军": cells[3].strip()
            }
            data.append(item)
            print(f"  排名{item['排名']}: {item['语言']} ({item['流行度']})")

    return {"headers": headers, "data": data}

def practice_4_css_selector(document):
    """
    练习4: CSS类选择器与属性提取
    目标: 通过class定位，提取data-id、img src等属性
    XPath: //div[@class="movie-card"]
    """
    print("\n" + "=" * 60)
    print("练习4: CSS类选择器与属性提取")
    print("-" * 60)

    movies = document.xpath('//div[contains(@class, "movie-card")]')

    data = []
    for movie in movies:
        # 提取 data-id 属性
        data_id = movie.get('data-id', '无')

        # 提取图片src
        img_src = movie.xpath('.//img[@class="movie-poster"]/@src')
        img_src = img_src[0] if img_src else '无'

        # 提取标题
        title = movie.xpath('.//div[@class="movie-title"]/text()')[0].strip()

        # 提取评分
        rating_text = movie.xpath('.//div[@class="movie-rating"]//text()')
        rating = ''.join(rating_text).strip()

        movie_data = {
            "ID": data_id,
            "标题": title,
            "评分": rating,
            "图片URL": img_src[:50] + "..." if len(img_src) > 50 else img_src
        }
        data.append(movie_data)
        print(f" ID:{data_id} | {title} | {rating}")

    return data


def practice_5_hidden_data(document):
    """
    练习5: 隐藏数据（display:none）
    目标: 提取页面上不可见但源码中存在的数据
    XPath: //div[@id="secretContent"]
    """
    print("\n" + "=" * 60)
    print("练习5: 隐藏数据（display:none）")
    print("-" * 60)

    # 直接提取隐藏区域的内容
    secret_items = document.xpath('//div[@id="secretContent"]//li')

    data = []
    for item in secret_items:
        # 用户名
        user = item.xpath('.//strong/text()')[0].strip() if item.xpath('.//strong/text()') else '匿名'

        # 时间
        time = item.xpath('.//span/text()')[0].strip() if item.xpath('.//span/text()') else ''

        # 评论内容
        text = item.xpath('.//p/text()')[0].strip() if item.xpath('.//p/text()') else ''

        comment = {
            "用户": user,
            "时间": time,
            "评论": text
        }
        data.append(comment)
        print(f" {user} ({time})")
        print(f" {text}")

    return data


def save_to_json(all_data, filename="extracted_data.json"):
    """保存提取结果到 JSON 文件"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"\n数据已保存到: {filename}")


def main():
    """主函数：运行所有练习"""
    print("🕷️" * 20)
    print("  爬虫练习靶场 - 数据提取程序")
    print("🕷️" * 20)


    # 运行所有练习
    results = {
        "练习1_基础表格": practice_1_basic_table(document),
        "练习2_嵌套列表": practice_2_nested_list(document),
        "练习3_不规则表格": practice_3_irregular_table(document),
        "练习4_电影卡片": practice_4_css_selector(document),
        "练习5_隐藏数据": practice_5_hidden_data(document)
    }

    # 保存结果
    save_to_json(results)

    print("\n" + "✅" * 30)
    print("所有练习完成！请检查 extracted_data.json 文件")
    print("✅" * 30)

    return results


if __name__ == "__main__":
    main()


