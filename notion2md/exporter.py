import os
import requests
from datetime import datetime


class PageBlockExporter:
    def __init__(self, url, client, blog_mode):
        self.client = client
        self.page = self.client.get_block(url)
        self.title = self.page.title
        self.bmode = blog_mode
        if self.bmode:
            self.md = self._page_header()
            self.file_name = self._set_filename()
        else:
            self.file_name = self.page.title
            self.md = ""
        self.image_dir = ""
        self.download_dir = ""
        self.sub_exporters = []

    def create_main_folder(self, directory):
        """create folder with file name

          Args:
            directory(Stirng): set empty by default.
        """
        self.dir = directory + self.title + '/'

        if not(os.path.isdir(self.dir)):
            os.makedirs(os.path.join(self.dir))

    def create_folder(self, directory):
        """create folder with directory

          Args:
            directory(Stirng): set empty by default.
        """
        self.dir = directory

        if not(os.path.isdir(self.dir)):
            os.makedirs(os.path.join(self.dir))

    def create_sub_folder(self):
        """create sub folder with current file name

          Args:
            directory(Stirng): set empty by default.
        """
        self.sub_dir = self.dir + 'subpage/'
        if not(os.path.isdir(self.sub_dir)):
            os.makedirs(os.path.join(self.sub_dir))

    def create_file(self):
        """create md file that md will be stored

          Returns:
            self.file(String): path of file
        """
        file_path = os.path.join(self.dir, self.file_name + '.md')
        self.file = open(file_path, 'w', encoding='utf-8')
        return file_path

    def write_file(self):
        """save markdown output in the file
        """
        self.file.write(self.md)
        self.file.close()

    def create_image_foler(self):
        """create image output directory
        """
        self.image_dir = os.path.join(self.dir, 'image/')
        if not(os.path.isdir(self.image_dir)):
            os.makedirs(os.path.join(self.image_dir))

    def image_export(self, url, count):
        """make image file based on url and count.

          Args:
            url(Stirng): url of image
            count(int): the number of image in the page

          Returns:
            image_path(String): image_path for the link in markdown
        """
        if self.image_dir is "":
            self.create_image_foler()
        image_path = self.image_dir + 'img_{0}.png'.format(count)
        r = requests.get(url, allow_redirects=True)
        open(image_path, 'wb').write(r.content)
        return image_path

    def create_download_foler(self):
        """create download output directory
        """
        self.download_dir = os.path.join(self.dir, 'download/')
        print(self.download_dir)
        if not(os.path.isdir(self.download_dir)):
            os.makedirs(os.path.join(self.download_dir))

    def downlaod_file(self, url, file_name):
        """download a file in the page.

          Args:
            url(Stirng): url of the downlaod file
            file_name(String): name of the file

          Returns:
            None
        """
        if self.download_dir is "":
            self.create_download_foler()

        try:
            download_path = self.download_dir + file_name
        except Exception as e:
            print(e)
        r = requests.get(url, allow_redirects=True)
        open(download_path, 'wb').write(r.content)

    def _page_header(self):
        """return the page's header formatted as Front Matter

          Returns:
            header(Stirng): return Front Matter header
        """
        header = "---\n"
        header += "layout: post\n"
        header += "title: \"{0}\"\n".format(self.title)
        try:
            header += "date: {0}\n".format(self._format_date())
        except:
            header += ""
        tags = self._get_tags()
        if len(tags) != 0:
            header += "tags:\n"
            for tag in tags:
                header += '- ' + tag + '\n'
        
        header += "categories: {0}\n".format(self._get_categories())
        header += "permalink: {0}\n".format(self._get_permalink())
        header += "author: {0}\n".format(self._get_author())
        header += "background: {0}\n".format(self._get_background())
        header += '---\n'
        return header

    def _get_tags(self):
        """return tags in the page

          Condition:
            "Tags" or "tags" property should exist in the page

          Returns:
            tags([String]): tags in "Tags or tags" property in the page
        """
        try:
            tags = self.page.get_property('tags')
        except:
            print("\n[Notice] '{0}' has no Tags".format(self.page.title))
            tags = []
        return tags

    def _get_categories(self):
        """return categories property in the page

          Condition:
            "Categories" or "categories" property should exist in the page

          Returns:
            categories([String]): categories in "Categories or categories" property in the page
        """
        try:
            categories = self.page.get_property('categories')
        except:
            print("\n[Notice] '{0}' has no Categories".format(self.page.title))
            categories = []
        return categories

    def _get_permalink(self):
        """return permalink property in the page

          Condition:
            "Permalink" or "permalink" property should exist in the page

          Returns:
            Permalink(String): Permalink in "Permalink or permalink" property in the page
        """
        try:
            permalink = self.page.get_property('permalink')
        except:
            print("\n[Notice] '{0}' has no Permalink".format(self.page.title))
            permalink = None
        return permalink

    def _get_author(self):
        """return author property in the page

          Condition:
            "Author" or "author" property should exist in the page

          Returns:
            Author(String): author in "Author or author" property in the page
        """
        try:
            author = self.page.get_property('author')
        except:
            print("\n[Notice] '{0}' has no Author".format(self.page.title))
            author = None
        return author

    def _get_background(self):
        """return background image property in the page

          Condition:
            "Background" or "background" property should exist in the page

          Returns:
            Background(String): background in "background or Background" property in the page
        """
        try:
            background = self.page.get_property('background')
        except:
            print("\n[Notice] '{0}' has no background".format(self.page.title))
            background = None
        return background

    def _format_date(self):
        """return created date in the page

          Condition:
            "created" or "Created" property should exit in the page

          Returns:
            formatted_date(String): formatted created date
        """
        date = self.page.get_property("postar_em")
        formatted_date = date.to_notion()[0][1][0][1]['start_date']
        return formatted_date

    def _set_filename(self):
        """return formatted file name

          Returns:
            file name(String): formatted_file_name
        """
        try:
            date_in_name = self._format_date() + "-"
        except:
            print("[Notice] '{0}' has no Created Date".format(self.page.title))
            date_in_name = ""
        file_name = date_in_name + self.title.replace(" ", "-")
        return file_name

    def page2md(self, page=None):
        """change notion's block to markdown string
        """
        params = {'tap_count':0,'img_count':0,'num_index':0}
        if page is None:
            page = self.page
        for i,block in enumerate(page.children):
            try:
                self.block2md(block,params)
            except Exception as e:
                self.md += ""
        self.md = self.md[:-1]

    def block2md(self,block,params):
        if params['tap_count'] != 0:
            self.md += '\n'
            for i in range(params['tap_count']):
                self.md += '\t'
        try:
            btype = block.type
        except:
            pass
        if btype != "numbered_list":
            params['num_index'] = 0
        try:
            bt = block.title
        except:
            pass
        if btype == 'header':
            self.md += "# " + block.title
        if btype == "sub_header":
            self.md += "## " + block.title
        if btype == "sub_sub_header":
            self.md += "### " + block.title
        if btype == 'page':
            self.create_sub_folder()
            sub_url = block.get_browseable_url()
            exporter = PageBlockExporter(sub_url, self.client, self.bmode)
            exporter.create_folder(self.sub_dir)
            sub_page_path = exporter.create_file()
            try:
                if "https:" in block.icon:
                    icon = "!"+link_format("", block.icon)
                else:
                    icon = block.icon
            except:
                icon = ""
            self.sub_exporters.append(exporter)
            self.md += icon + link_format(exporter.file_name, sub_page_path)
        if btype == 'text':
            try:
                self.md += "{: style=\"text-align: justify\" }\n"
                self.md += block.title
            except:
                self.md += ""
        if btype == 'bookmark':
            self.md += link_format(bt, block.link)
        if btype == "file":
            self.md += link_format("Para mais informações clique aqui.", block.source)
        if btype == "video" or btype == "audio" or btype == "pdf" or btype == "gist":
            self.md += link_format(block.source, block.source)
        if btype == "bulleted_list" or btype == "toggle":
            self.md += '- '+ block.title
        if btype == "numbered_list":
            params['num_index'] += 1
            self.md += str(params['num_index'])+'. '+ block.title
        if btype == "code":
            self.md += "``` "+block.language.lower()+"\n"+block.title+"\n```"
        if btype == "equation":
            self.md += "$$"+block.latex+"$$"
        if btype == "divider":
            self.md += "---"
        if btype == "to_do":
            if block.checked:
                self.md += "- [x] " + bt
            else:
                self.md += "- [ ]" + bt
        if btype == "quote":
            self.md += "> "+bt
        if btype == "column" or btype == "column_list":
            self.md += ""
        if btype == "collection_view":
            collection = block.collection
            self.md += self.make_table(collection)
        if block.children and btype != 'page':
            params['tap_count'] += 1
            for child in block.children:
                self.block2md(child,params)
            params['tap_count'] -= 1
        if params['tap_count'] == 0:
            self.md += "\n\n"

    def make_table(self, collection):
        columns = []
        row_blocks = collection.get_rows()
        for proptitle in row_blocks[0].schema:
            prop = proptitle['name']
            if prop == "Name":
                columns.insert(0, prop)
            else:
                columns.append(prop)
        table = []
        table.append(columns)
        for row in row_blocks:
            row_content = []
            for column in columns:
                if column == "Name" and row.get("content") is not None:
                    content = self.page2md(row)
                else:
                    content = row.get_property(column)
                if str(type(content)) == "<class 'list'>":
                    content = ', '.join(content)
                if str(type(content)) == "<class 'datetime.datetime'>":
                    content = content.strftime('%b %d, %Y')
                if column == "Name":
                    row_content.insert(0, content)
                else:
                    row_content.append(content)
            table.append(row_content)
        return table_to_markdown(table)


def link_format(name, url):
    """make markdown link format string
    """
    return "["+name+"]"+"("+url+")"


def table_to_markdown(table):
    md = ""
    md += join_with_vertical(table[0])
    md += "\n---|---|---\n"
    for row in table[1:]:
        if row != table[1]:
            md += '\n'
        md += join_with_vertical(row)
    return md


def join_with_vertical(list):
    return " | ".join(list)


def filter_inline_math(block):
    """This function will get inline math code and append it to the text
    """
    text = ""
    elements = block.get("properties")["title"]
    for i in elements:
        if i[0] == "⁍":
            text += "$$"+i[1][0][1]+"$$"
        else:
            text += block.title
    return text

def filter_source_url(block):
    try:
        return block.get('properties')['source'][0][0]
    except:
        return block.title
