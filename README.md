# Symmetric traveling salesman problem (TSP)

## benchmark 测试用例

德国海德堡大学（Heidelberg University）教授Gerhard Reinelt维护的网站[TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)中包含了TSP问题的benchmark数据。

```commandline
gzip -d *.gz
```

为EUC_2D类型且城市数小于等于1000的测试用例，共计48个。

## parser 解析器

读取文本文件，以`Dict({__index__: (__x__, __y__)})`形式存储。

## algorithm 演算法


### 参考资料：
<iframe width="560" height="315" src="https://www.youtube.com/embed/GiDsjIBOVoA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
1. https://youtu.be/GiDsjIBOVoA
2. 