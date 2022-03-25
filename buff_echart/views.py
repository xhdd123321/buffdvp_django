import json
from random import randrange

from django.apps import apps
from django.http import HttpResponse, JsonResponse
from pyecharts.charts import Bar, Page, Pie
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from pyecharts import options as opts
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from buff_data.models import Chart
from common.Mypagination import MyPageNumberPagination
from .analyzers import Analyzer
from .apps import BuffEchartConfig as AppConfig
from .serializers import EchartSerializer

app_config = apps.get_app_config(AppConfig.name)

toolbox_opts = opts.global_options.ToolBoxFeatureOpts(
    save_as_image={"show": True, "title": "save as image", "type": "png"},
    restore={"show": False},
    data_zoom={"show": False},
    magic_type={"show": False},
    brush={"show": False},
)


def bar_base() -> Bar:
    c = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
            .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
            .dump_options_with_quotes()
    )
    return c


def bar_by_two_list(one: list, two: list, title: str) -> Bar:
    c = (
        Bar()
            .add_xaxis(one)
            .add_yaxis("count", two)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Bar-{0}".format(title), subtitle="count统计表"),
                toolbox_opts=opts.ToolboxOpts(feature=toolbox_opts),
            )
    )
    return c.dump_options_with_quotes()


def pie_by_two_list(one: list, two: list, title: str) -> Pie:
    data_pair = [list(z) for z in zip(one, two)]
    data_pair.sort(key=lambda x: x[1])
    c = (
        Pie(init_opts=opts.InitOpts(width="1600px", height="800px", bg_color="#2c343c"))
            .add(
            series_name="count",
            data_pair=data_pair,
            rosetype="radius",
            radius="55%",
            center=["50%", "50%"],
            label_opts=opts.LabelOpts(is_show=False, position="center"),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Pie-{0}".format(title),
                subtitle="count统计",
                pos_left="center",
                pos_top="20",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            toolbox_opts=opts.ToolboxOpts(feature=toolbox_opts),
        )
            .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            label_opts=opts.LabelOpts(color="rgba(255, 255, 255, 0.3)"),
        )
    )
    return c.dump_options_with_quotes()


class EchartViewSet(GenericViewSet):
    """
    返回 echart生成 数据
    """
    serializer_class = EchartSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = MyPageNumberPagination

    # authentication_classes = (JWTAuthentication,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chart_id = serializer.validated_data['chart_id']
        try:
            chart_obj = Chart.objects.get(id=chart_id)
        except Chart.DoesNotExist:
            raise NotFound("待分析图表不存在")

        # 生成数据
        bar_list = list()
        pie_list = list()
        ana = Analyzer(chart_obj)
        res_list = ana.analysis_by_count()
        for item in res_list:
            title = item[1]
            content_dict = item[0]
            a_list = list(content_dict.keys())
            b_list = list(content_dict.values())
            bar = json.loads(bar_by_two_list(a_list, b_list, title))
            pie = json.loads(pie_by_two_list(a_list, b_list, title))
            bar_list.append(bar)
            pie_list.append(pie)

        res = {
            "bar_list": bar_list,
            "pie_list": pie_list
        }
        return Response(res)


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/index.html").read())
