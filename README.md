# Symmetric traveling salesman problem (TSP)

## benchmark 测试用例

德国海德堡大学（Heidelberg University）教授Gerhard
Reinelt维护的网站[TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)中包含了TSP问题的benchmark数据。

```commandline
gzip -d *.gz
```

为EUC_2D类型且城市数小于等于1000的测试用例，共计48

## parser 解析器

读取文本文件，以`Dict({__index__: (__x__, __y__)})`形式存储。

## algorithm 演算法

### 基石算法实现

求解旅行商问题的算法可分为两类：完整算法和近似算法。
1. 完整算法保证给出最优解，但计算时间太长，仅可用于计算较小规模实例；
2. 近似算法（邻域搜索、遗传、模拟退火、粒子群算法等），或许有可能在短时间内，给出相当接近最优解的近似解。

- [x] 最近邻算法（Nearest Neighbors Algorithm）

- [ ] 检查“环”与“度”的贪婪算法（Greedy Heuristic Algorithm）

- [ ] 基于“最小生成树”的算法（Nicos Christofides Algorithm）

- [ ] 基于“交换”的邻域优化算法（Random Swapping）：2-opt，3-opt，k-opt

- [ ] 模拟“退火”的拟物优化算法（Simulated Annealing）：绝处逢生。

- [ ] 模拟“蚁群”的拟物优化算法（Ant-Colony Optimization）：概率分布；距离+奖励值/信息素，超参数。

- [ ] 王磊算法：

### 改进策略实现

- [ ] 先基本算法：贪婪算法【非随机性近似算法：贪心插入法】、后邻域搜索：随机算法【随机性近似算法：模拟退火】
- [ ] 贪婪算法【非随机性近似算法：最近邻】，用于计算最后的长度（优度）
 逐层优美度枚举算法中套基本算法：按照概率分布，枚举下一步取哪一个点（N个），按照基本算法计算优美度，取优美度最大的。

### 参考资料：

1. 王磊-求解旅行商问题的拟物拟人算法研究计算结果，2023年6月
2. 王磊.求解工件车间调度问题的一种高效近似算法.2006.华中科技大学,PhD dissertation.
3. 王磊,尹爱华."求解二维矩形Packing问题的一种优美度枚举算法." 中国科学:信息科学 45.09(2015):1127-1140.
4. [The Traveling Salesman Problem: When Good Enough Beats Perfect](https://youtu.be/GiDsjIBOVoA)
5. [MIT Approximation Algorithms: Traveling Salesman Problem](https://youtu.be/zM5MW5NKZJg)
6. [算法进阶课——模拟退火](https://www.acwing.com/activity/content/32/)