# GEOFlow 前台模块与变量地图

本文档是 `geoflow-template` 的核心参考。目标不是解释业务，而是定义：当前 GEOFlow 前台页面由哪些稳定模块组成、依赖哪些变量和函数、哪些位置可以替换样式、哪些契约必须保留。

工作区基线：
- 代码库：标准 GEOFlow PHP 工作区（根目录包含 `index.php`、`article.php`、`category.php`、`archive.php`、`includes/header.php`）
- 正式前台入口：
  - `index.php`
  - `article.php`
  - `category.php`
  - `archive.php`
  - `includes/header.php`
  - `includes/footer.php`

## 1. 全站稳定契约

### 1.1 正式页面

- 首页：`index.php`
- 文章详情页：`article.php`
- 分类页：`category.php`
- 归档页：`archive.php`
- 公共头部：`includes/header.php`
- 公共底部：`includes/footer.php`

### 1.2 样式与资源

- 全局样式：
  - `assets/css/style.css`
  - `assets/css/custom.css`
- 图标：Lucide
- 页面层仍依赖 Tailwind CDN

### 1.3 路由契约

由 `router.php` 负责，当前正式前台路由必须保留：

- `/`
- `/article/{slug}`
- `/category/{slug|id}`
- `/archive`
- `/archive/{year}/{month}`
- `/search/{term}` 或首页搜索模式

### 1.4 必须保留的核心函数

来自 `includes/functions.php` 与 `includes/seo_functions.php`：

- `get_categories()`
- `get_featured_articles($limit = 6)`
- `search_articles($search, $page = 1, $per_page = 12)`
- `get_search_count($search)`
- `get_category_by_id($id)`
- `get_articles_by_category($category_id, $page = 1, $per_page = 12)`
- `get_category_article_count($category_id)`
- `get_article_by_slug($slug)`
- `get_public_article_by_id($id)`
- `get_article_tags($article_id)`
- `get_related_articles($article_id, $category_id, $limit = 4)`
- `get_site_stats()`
- `get_active_article_detail_ad()`
- `markdown_to_html($text)`
- `generate_pagination($current_page, $total_pages, $base_url)`
- `site_setting_value($key, $default = '')`
- `output_site_head_extras()`
- `generate_page_title(...)`
- `generate_page_description(...)`
- `generate_page_keywords(...)`
- `geo_absolute_url($path = '/')`
- `generate_article_structured_data(...)`
- `generate_category_structured_data(...)`
- `generate_website_structured_data()`
- `generate_collection_structured_data(...)`
- `generate_breadcrumb_structured_data(...)`
- `build_article_geo_summary(...)`
- `build_collection_geo_summary(...)`

## 2. 全站公共变量

这些变量跨页面重复出现，是模板系统必须兼容的输入：

- `site_title`
- `site_subtitle`
- `site_description`
- `site_keywords`
- `site_logo`
- `categories`
- `app_locale()`
- `app_html_lang()`
- `admin_url()`

页面级公共输出：

- `page_title`
- `page_description`
- `page_keywords`
- `canonical_url`
- `structured_data_blocks`

## 3. 公共头部模块

文件：
- `includes/header.php`

### 3.1 模块组成

- Logo / 站点名称
- 桌面导航
- 分类下拉菜单
- 移动端菜单
- 后台入口按钮

### 3.2 依赖变量

- `site_title`
- `site_logo`
- `categories`
- `request_path`
- `is_home`
- `is_archive`

### 3.3 模板可替换范围

- Logo 容器样式
- 顶部导航布局
- 下拉菜单视觉
- 移动端菜单样式
- 分类项视觉

### 3.4 不可破坏点

- 分类列表仍来自 `get_categories()`
- 后台入口仍保留 `admin_url()`
- 导航仍要能覆盖首页、分类、归档、后台入口

## 4. 公共底部模块

文件：
- `includes/footer.php`

### 4.1 模块组成

- 版权信息块

### 4.2 依赖变量

- `footer_copyright_text`
- `app_locale()`
- `site_setting_value('copyright_info' / 'copyright_text')`

### 4.3 模板可替换范围

- 布局、对齐、配色、边框、间距

## 5. 首页模块地图

文件：
- `index.php`

### 5.1 页面模式

首页并不总是同一种 UI，而是三种模式：

- 默认首页聚合模式
- 搜索结果模式
- 分类过滤模式（兼容 query 参数）

### 5.2 关键变量

- `category_id`
- `search`
- `page`
- `per_page`
- `site_title`
- `site_subtitle`
- `site_description`
- `site_keywords`
- `featured_limit`
- `site_stats`
- `category`
- `categories`
- `featured_articles`
- `articles`
- `total_count`
- `total_pages`
- `view_title`

### 5.3 模块组成

- `home.hero`
  - 站点主标题
  - 站点副标题 / 描述
- `home.featured_list`
  - 精选文章 section label
  - 精选文章卡片列表
- `home.latest_list`
  - 最新文章 section label
  - 文章卡片列表
- `home.search_breadcrumb`
  - 搜索状态面包屑
- `home.category_intro`
  - 分类标题和描述
- `home.article_card`
  - 日期
  - 分类 chip
  - 推荐 badge
  - 标题
  - 摘要
  - 标签
  - 阅读全文按钮
- `home.empty_state`
- `home.pagination`

### 5.4 首页文章卡片依赖字段

每张文章卡片至少依赖：

- `article.id`
- `article.slug`
- `article.title`
- `article.excerpt`
- `article.content`
- `article.category_id`
- `article.category_name`
- `article.published_at`
- `article.created_at`
- `article.is_featured`
- `article_tags[]`

### 5.5 可模板化结论

首页最适合模板化的稳定模块：

- Hero
- Section header
- Featured article card
- Standard article card
- Empty state
- Pagination shell

## 6. 文章详情页模块地图

文件：
- `article.php`

### 6.1 关键变量

- `slug`
- `article_id`
- `article`
- `article_tags`
- `related_articles`
- `article_detail_ad`
- `article_content`
- `article_excerpt`
- `article_content_summary`
- `page_title`
- `page_description`
- `page_keywords`
- `canonical_url`

### 6.2 模块组成

- `article.breadcrumb`
- `article.category_chip`
- `article.hero`
  - 标题
  - 发布时间
  - 摘要框
- `article.prose_shell`
  - Markdown 转 HTML 的正文容器
- `article.tags`
- `article.related_articles`
  - 标题
  - 排名数字
  - 相关文章列表
- `article.sticky_ad`
  - 关闭按钮
  - badge
  - title
  - copy
  - CTA button

### 6.3 文章详情广告位字段

来自 `get_active_article_detail_ad()`：

- `id`
- `name`
- `badge`
- `title`
- `copy`
- `button_text`
- `button_url`
- `enabled`

### 6.4 不可破坏点

- 正文必须继续来自 `markdown_to_html($article_content)`
- 相关文章必须继续来自 `get_related_articles(...)`
- 广告位数据结构不能丢字段
- slug 路由必须保持 `/article/{slug}`

## 7. 分类页模块地图

文件：
- `category.php`

### 7.1 关键变量

- `category_slug`
- `category_id`
- `page`
- `per_page`
- `category`
- `categories`
- `articles`
- `total_count`
- `total_pages`
- `page_title`
- `page_description`
- `canonical_url`

### 7.2 模块组成

- `category.breadcrumb`
- `category.page_intro`
  - 分类名称
  - 分类描述
- `category.article_list`
- `category.article_card`
- `category.empty_state`
- `category.pagination`

### 7.3 分类页文章卡片依赖字段

- `article.slug`
- `article.title`
- `article.excerpt`
- `article.content`
- `article.published_at`
- `article.is_featured`
- `article_tags[]`
- `category.name`

## 8. 归档页模块地图

文件：
- `archive.php`

### 8.1 页面模式

- `archive.overview`
- `archive.month_detail`

### 8.2 关键变量

- `year`
- `month`
- `page`
- `per_page`
- `archives`
- `articles`
- `total_count`
- `total_pages`
- `archive_title`
- `canonical_url`

### 8.3 模块组成

- `archive.breadcrumb`
- `archive.page_intro`
- `archive.overview_year_group`
- `archive.overview_row`
  - 年
  - 月
  - 文章数
- `archive.month_article_list`
- `archive.month_article_card`
- `archive.empty_state`
- `archive.pagination`

## 9. SEO / Head 注入模块

页面统一依赖：

- `output_site_head_extras()`
- `output_structured_data_blocks(...)`

站点级设置影响前台 head：

- `site_name`
- `site_description`
- `site_keywords`
- `site_favicon`
- `analytics_code`
- `seo_title_template`
- `seo_description_template`

这些属于模板系统必须兼容的 head 层配置，不适合在模板克隆中删除。

## 10. 当前可安全模板化的模块清单

这是最适合做“参考站点复刻映射”的单元：

- `header`
- `footer`
- `home.hero`
- `home.section_header`
- `home.article_card`
- `category.article_card`
- `archive.overview_row`
- `archive.month_article_card`
- `article.hero`
- `article.prose_shell`
- `article.related_articles`
- `article.sticky_ad`
- `empty_state`
- `pagination_shell`

## 11. 当前不应直接模板化替换的部分

- 文章、分类、作者、标签等业务数据查询逻辑
- slug 路由规则
- SEO / structured data 生成逻辑
- Markdown 正文渲染入口
- 广告位字段结构
- GEO summary 生成逻辑

## 12. 主题包生成的最小映射目标

如果要从外部 URL 复刻成 GEOFlow 模板，最低要生成这些映射：

- `header`
- `footer`
- `home.hero`
- `home.featured_list`
- `home.article_card`
- `category.article_card`
- `article.hero`
- `article.prose_shell`
- `article.related_articles`
- `article.sticky_ad`
- `archive.overview_row`
- `archive.article_card`

## 13. 对后续系统实现的约束

后台“网站模板”功能如果后续要做，建议只做：

- 模板注册
- 模板预览
- 模板启用

不建议让后台直接编辑任意模板源码。更稳的方式是：

- skill 生成模板包
- 系统识别模板包
- 后台只负责选择、预览、启用
