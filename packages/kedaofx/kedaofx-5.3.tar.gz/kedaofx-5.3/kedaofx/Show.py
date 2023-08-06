def pre():
    """
    :return: 初始化notebook
    """
    from pyecharts.globals import CurrentConfig, NotebookType
    CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB
    import numpy as np

    from pyecharts.charts import Scatter

    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    scatter = Scatter()
    scatter.add_xaxis(xaxis_data=x)
    scatter.add_yaxis(series_name='sin', y_axis=y)

    return scatter.load_javascript()


def show_null(self, ops_int=None, ops_str=None):
    """
    :param self: 数据
    :param ops_int:
    :param ops_str:
    :return: 图形
    """

    global bar
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.commons.utils import JsCode
    import numpy as np
    from pyecharts.globals import CurrentConfig, NotebookType
    CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB
    CurrentConfig.ONLINE_HOST = 'https://assets.pyecharts.org/assets/'

    null = self.isnull().sum().tolist()

    null_int = (self == ops_int).sum().tolist()
    null_str = (self == ops_str).sum().tolist()
    if max(null) + max(null_int) + max(null_str) == 0:
        print('无空值')
    else:

        null_all = np.sum([null, null_int, null_str], axis=0).tolist()
        null_end = []
        x_columns = []
        x_i = self.columns
        for i in range(0, len(self.columns)):
            if null_all[i] == 0:
                pass
            else:
                null_end.append(null_all[i])
                x_columns.append(x_i[i])
        max_all = len(self)
        line_null = []
        for i in range(0, len(null_end)):
            line_null.append(float("%.2f" % ((null_end[i] / max_all) * 100)))

        X = x_columns
        colors = ['#8A54B6', '#5F7FC8', '#E4002C', '#E7D8C4']
        values = line_null
        # 指定柱子颜色的js代码
        color_function = """
                function (params) {
                    if (params.value <= 20)
                        return '#00B642';
                    else if (params.value > 20 && params.value <= 80)
                        return '#FF8A00';
                    else return '#E4002C';
                }
                """

        bar = (
            Bar(opts.InitOpts(bg_color='white'))
            .add_xaxis(X)
            .add_yaxis(""
                       , values
                       , category_gap="40%"
                       , itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function))

                       )

            .set_series_opts(label_opts=opts.LabelOpts(is_show=False, formatter="{c}%"),
                             markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=20, name="20%"),
                                                                   opts.MarkLineItem(y=80, name="80%"),
                                                                   opts.MarkLineItem(y=50, name="50%")
                                                                   ],
                                                             label_opts=opts.LabelOpts(formatter="{c}%"),
                                                             linestyle_opts=opts.LineStyleOpts(color='#CD4A4F')

                                                             ),

                             )

            .set_global_opts(title_opts=opts.TitleOpts(title="各个商品销量比较"))
            .set_global_opts(
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    name="",
                    min_=0,
                    max_=100,
                    position="left",
                    offset=0,

                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color='black')
                    ),
                    axislabel_opts=opts.LabelOpts(formatter=("{value}%")),
                ),

                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),

                # 坐标轴显示不全处理
                xaxis_opts=opts.AxisOpts(name_rotate=60, axislabel_opts={"rotate": 45},
                                         name_textstyle_opts=opts.TextStyleOpts(font_size=100),
                                         axisline_opts=opts.AxisLineOpts(
                                             linestyle_opts=opts.LineStyleOpts(color='black')))
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="空值查看"))

        )

    bar.load_javascript()
    return bar.render_notebook()
