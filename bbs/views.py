from django.shortcuts import render

#TODO:ここでDRF仕様のビュークラスと通常のビュークラスを切り替え
from django.views import View
#from rest_framework.views import APIView as View

from django.http.response import JsonResponse
from django.template.loader import render_to_string

from .models import Topic
from .forms import TopicForm

class IndexView(View):

    def get(self, request, *args, **kwargs):

        topics  = Topic.objects.all()
        context = { "topics":topics }

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):

        json    = { "error":True }

        form    = TopicForm(request.POST)

        if not form.is_valid():
            print("バリデーションNG")
            return JsonResponse(json)

        form.save()


        #=====ここからレンダリング処理==========================
        #(PUTやDELETEなどでも、同様のレンダリング行うので、この部分はこのビュークラスのメソッドとして呼び出せるようにしたほうが良い。)

        context             = {}
        context["topics"]   = Topic.objects.all()

        json["content"]     = render_to_string("bbs/content.html",context,request)
        json["error"]       = False

        #=====ここまでレンダリング処理==========================


        return JsonResponse(json)

    def delete(self, request, *args, **kwargs):
        
        json    = { "error":True }

        if "pk" not in kwargs:
            return JsonResponse(json)

        topic   = Topic.objects.filter(id=kwargs["pk"]).first()

        if not topic:
            return JsonResponse(json)


        #=======ここからリクエストボディの解析=======

        #DRFを使用しない場合、DELETE、PUT、PATCHメソッドのデータはrequest.bodyより参照する。(クエリ文字列になっているのでデコードと解析をする必要がある。)
        print(request.body)
        print(type(request.body))

        raw_data    = request.body.decode("utf-8")
        data_list   = raw_data.split("&")

        for data in data_list:
            data    = data.split("=")
            print("Key:",data[0], "Value:",data[1])

        #=======ここまでリクエストボディの解析=======


        topic.delete()

        json["error"]   = False

        return JsonResponse(json)

index   = IndexView.as_view()

