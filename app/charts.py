#coding:utf8

# test graph
def test_graph():
    from pyecharts import Line, Style

    style = Style(
        width='100%'
    )

    attr,v1,v2,v3,v4 = [],[],[],[],[]
    line = Line("cpu们",renderer='svg')
    # ** style.init_style
    line.chart_id = 'cpus'
    line.width = '100%'
    line.add("cpu1", attr, v1, is_smooth="True", is_toolbox_show=False)
    line.add("cpu2", attr, v2, is_smooth="True")
    line.add("cpu3", attr, v3, is_smooth="True")
    line.add("cpu4", attr, v4, is_smooth="True")
    return line.render_embed()