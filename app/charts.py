# coding:utf8
from pyecharts import Bar, Pie


# 四核CPU折线图
def test_graph():
    from pyecharts import Line, Style

    style = Style(
        width='100%'
    )

    attr, v1, v2, v3, v4 = [], [], [], [], []
    line = Line("cpu们", renderer='svg')
    # ** style.init_style
    line.chart_id = 'cpus'
    line.width = '100%'
    line.add("cpu1", attr, v1, is_smooth="True", is_toolbox_show=False)
    line.add("cpu2", attr, v2, is_smooth="True")
    line.add("cpu3", attr, v3, is_smooth="True")
    line.add("cpu4", attr, v4, is_smooth="True")
    return line.render_embed()


# Server Status: CPU, Memory, Network
def server_status():
    attr = ["CPU", "Memory", "Network"]
    v1 = [0, 0, 0]
    bar = Bar()
    bar.chart_id = "serverow"
    bar.width = "100%"
    label_color = ["#a0a7e6", "#3fb1e3", "#6be6c1", "#626c91", "#c4ebad"]
    bar.add("Win10", attr, v1, yaxis_max=100,
            is_stack=True, is_label_show=True,
            bar_category_gap="5%", label_color=label_color)
    return bar.render_embed()


def home_basic(home):
    attr = ["债务","资产", "现金"]
    v1 = [home.debt, home.asset, home.cash]
    pie = Pie("资产概览")
    pie.id = "home_basic"
    pie.width = "100%"
    pie.add("",attr,v1,is_label_show=True)
    return pie.render_embed()