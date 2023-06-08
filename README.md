# Symmetric traveling salesman problem (TSP)

## description 问题描述

旅行商问题是一个典型的NP难度问题，易于描述却难于求解。

1. 旅行商问题的类自然语言描述如下：给定$`n`$个城市，对这$`n`$个城市中的每两个城市来说，从一个城市到另一个城市所走的路程是已知的正实数（符合三角形三条边关系定则），其中$`n`$是已知的正整数，$`n \ge 3`$。这$`n`$个城市的全排列共有$`n!`$的阶乘个。每一个这$`n`$个城市的全排列都恰好对应着一种走法：从全排列中的第一个城市走到第二个城市，……，从全排列中的第$`n-1`$个城市走到第$`n`$个城市，从全排列中的第$`n`$个城市回到第一个城市。要求给出一个这$`n`$个城市的全排列$`\sigma`$，使得在$`n!`$个全排列中，全排列$`\sigma`$对应的走法所走的路程是最短的（严格来讲，由于起点任意、顺逆时针等价，问题复杂度为$`\frac{\left(n-1\right)!}{2}`$）。
2. 旅行商问题的形式化描述：给定一个有向完全图$`G=\left(V,A\right)`$，其中集合$`V=v_1,\ldots,v_n`$是顶点集合，每个顶点代表一个城市，n是顶点数（$`n\ge 3`$），集合$`E=\left(v_i,v_j\right)|v_i,v_j\in V,v_i\neq v_j`$是有向边集合。$`c_{ij}`$是有向边$`\left(v_i,v_j\right)`$的长度，$`c_{ij}`$是已知的正实数，其中$`\left(v_i,v_j\right)\in E`$。集合$`\Sigma`$是顶点全排列的集合，共有$`n!`$元素。$`\sigma`$是所有顶点的一个全排列，$`\sigma=\left(\sigma\left(1\right),\ldots,\sigma\left(n\right)\right)`$，$`\sigma\in\Sigma`$， $`\sigma\left(i\right)\in V`$，$`1\le i\ \le n`$。 对应着一条遍历所有顶点的回路：从顶点$``$走到顶点$``$，……，从顶点$``$走到顶点$``$，从顶点$``$回到顶点$``$。全排列$``$所对应的回路的长度记为$``$，$``$。目标是给出所有顶点的一个全排列$``$，使得$``$。

每一对顶点$``$和$``$来说，都有$``$成立，那么称问题是对称的（Symmetric traveling salesman problem）；否则称问题是非对称的（Asymmetric traveling salesman problem）。

## benchmark 测试用例

海德堡大学（Heidelberg University）教授Gerhard
Reinelt维护的网站[TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)包含TSP问题的benchmark数据。

```commandline
gzip -d *.gz
```

为EUC_2D类型且城市数小于等于1000的测试用例，共计48个。

## parser 解析器

读取文本文件，转化为`Dict({__index__: (__x__, __y__)})`。

## algorithm 演算法

### 基石算法实现

求解旅行商问题的算法可分为两类：完整算法和近似算法。

1. 完整算法保证给出最优解，但计算时间太长，仅可用于计算较小规模实例；
2. 近似算法，或许有可能在短时间内，给出相当接近最优解的近似解。非随机性近似算法包括构建式启发/贪婪算法，克里斯托菲德斯算法；随机性近似算法包括随机局域搜索、模拟退火、遗传算法、粒子群算法等。

对于近似算法求最小值问题，设$`Opt`$是最优解，x表示某算法给出的一个解，一般规定，$`Opt\le x\ \le\alpha\times Opt`$，$`\alpha`$记为该算法的近似比，可用于评价算法优劣。拟物仿生万用启发算法（又称元启发算法，metaheuristic），虽然有可能得出比较好的近似解，但往往不涉及在最差情况下的效率证明。基于“最小生成树”的经典非随机性近似算法有两种，分别符合2和1.5的近似比。

- [ ] 构建式启发/贪婪算法（Constructive heuristics）：主要是逐步插入点（边），最后得到一个包含所有城市的回路。

- [ ] 克里斯托菲德斯算法（Christofides–Serdyukov algorithm）：可证明，最差情况下，该近似算法所得回路长度不会超过最优回路长度的1.5倍。

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
7. 