# Symmetric traveling salesman problem (TSP)

## description 问题描述

🤯旅行商问题是一个典型的NP难度问题，可描述为平面上给定n个点，每两点之间的直线距离是已知的正实数，从某一个起点出发，经过其余点恰好一次，最后回到起点。要求给出一种走法，使得回路的长度最短。

1. 旅行商问题的类自然语言描述如下：给定$`n`$个城市，对这$`n`$个城市中的每两个城市来说，从一个城市到另一个城市所走的路程是已知的正实数，其中$`n`$是已知的正整数，$`n \ge 3`$。这$`n`$个城市的全排列共有$`n!`$的阶乘个。每一个这$`n`$个城市的全排列都恰好对应着一种走法：从全排列中的第一个城市走到第二个城市，……，从全排列中的第$`n-1`$个城市走到第$`n`$个城市，从全排列中的第$`n`$个城市回到第一个城市。要求给出一个这$`n`$个城市的全排列$`\sigma`$，使得在$`n!`$个全排列中，全排列$`\sigma`$对应的走法所走的路程是最短的。
> ▶️符合三角形三条边关系定则
> 
> ⬇️严格来讲，由于起点任意、顺逆时针等价，问题复杂度为$`\frac{\left(n-1\right)!}{2}`$

2. 旅行商问题的形式化描述：给定一个有向完全图$`G=\left(V,A\right)`$，其中集合$`V=v_1,\ldots,v_n`$是顶点集合，每个顶点代表一个城市，n是顶点数（$`n\ge 3`$），集合$`E=\left(v_i,v_j\right)|v_i,v_j\in V,v_i\neq v_j`$是有向边集合。 $`d_{ij}`$是有向边$`\left(v_i,v_j\right)`$的长度，$`d_{ij}`$是已知的正实数，其中$`\left(v_i,v_j\right)\in E`$。集合$`\Sigma`$是顶点全排列的集合，共有$`n!`$元素。$`\sigma`$是所有顶点的一个全排列，$`\sigma=\left(\sigma\left(1\right),\ldots,\sigma\left(n\right)\right)`$，$`\sigma\in\Sigma`$， $`\sigma\left(i\right)\in V`$，$`1\le i\ \le n`$。 $`\sigma`$对应着一条遍历所有顶点的回路：从顶点$`\sigma(1)`$走到顶点$`\sigma(2)`$，……，从顶点$`\sigma(n-1)`$走到顶点$`\sigma(n)`$，从顶点$`\sigma(n)`$回到顶点$`\sigma(1)`$。全排列$`\sigma`$所对应的回路的长度记为$`H(\sigma)`$，$`H(\sigma)=d_{\sigma(1) \sigma(2)} + ... + d_{\sigma(n-1) \sigma(n)} + d_{\sigma(n) \sigma(1)}`$。目标是给出所有顶点的一个全排列$`\sigma^*`$，使得$`H(\sigma^*)= \underset{\sigma \in \Sigma}{\min} (H(\sigma))`$。

> 🪞每一对顶点$`v_i`$ 和 $`v_j`$来说，都有$`d_{ij} = d_{ji}`$成立，那么称问题是对称的（Symmetric traveling salesman problem）； 否则称问题是非对称的（Asymmetric traveling salesman problem）。

## benchmark 测试用例

⏱️海德堡大学（Heidelberg University）教授Gerhard
Reinelt维护的网站[TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)包含TSP问题的benchmark数据。

```commandline
gzip -d *.gz
```

🧮为EUC_2D类型且城市数小于等于1000的测试用例，共计48个。

## parser 解析器

读取文本文件，转化为`Dict({__index__: (__x__, __y__)})`。

## algorithm 演算法

### fundamental 基石算法实现

🧄求解旅行商问题的算法可分为两类：完整算法和近似算法。

1. 完整算法保证给出最优解，但计算时间太长，仅可用于计算较小规模实例；
2. 近似算法，或许有可能在短时间内，给出相当接近最优解的近似解。非随机性近似算法包括构建式启发/贪婪算法，克里斯托菲德斯算法；随机性近似算法包括随机局域搜索、模拟退火、遗传算法、粒子群算法等。

#### 构建式启发/贪婪算法（Constructive heuristics）

主要是逐步插入点（边），最后得到一个包含所有城市的回路。例如：
+ 最近邻点算法：首先选择一个城市作为起点，然后用贪心法，每步均选择距离当前所在城市最近的未访问城市，最后回到起点。
+ 用贪心法选择符合要求的长度最短的边加入边集，直至边集构成一个哈密尔顿回路。要求如下：添加该边后，无法形成长度小于城市（顶点）数目的环，也无法形成“某城市（顶点）的度大于2”的格局。
+ “王磊”基本算法：首先生成一个3城市回路，然后依照一定次序，用贪心法将未访问城市插入回路，选择部分回路长度最短的动作，最后，得到包含所有城市的回路。

#### 克里斯托菲德斯算法（Christofides–Serdyukov algorithm）

可证明，最差情况下，该近似算法所得回路长度不会超过最优回路长度的**1.5**倍。

> 对于近似算法求最小值问题，设$`Opt`$是最优解，x表示某算法给出的一个解，一般规定，$`Opt\le x\ \le\alpha\times Opt`$，$`\alpha`$记为该算法的近似比，可用于评价算法优劣。 
> 
> 拟物仿生万用启发算法（又称元启发算法，metaheuristic），虽然有可能得出比较好的近似解，但往往不涉及在最差情况下的效率证明。

✍️基于“最小生成树”的经典非随机性近似算法有两种，分别符合`2`和`1.5`的近似比。

##### 近似比为2的算法（2-Approximation）

1. 定义：$`S`$代表一系列边（允许重边），$`c\left(S\right)`$代表各边权重（长度）之和。
2. 定义：$`H_G^\ast`$为无向多重图$`G`$上，长度最短的哈密尔顿回路（Hamiltonian Cycle），即途中经过所有点且只经过一次。
3. 构造最小生成树$`T，根据最小权生成树定义，$`c\left(H_G^\ast\right)\geq c\left(H_G^\ast-e\right)\geq c\left(T\right)`$。 
4. 按深搜次序记录回路$`C，下探一次，回溯一次，因此$`c\left(C\right)=2\times c\left(T\right)`$。例如，1，2，3，2，4，2，1，5，1，6，1。 
5. 搭桥（short-cut/bypass）略过重复访问的点（起点终点不删）得到符合问题描述的新回路$`C^\prime`$（最后回到起点），例如，1，2，3，4，5，6，1。 
6. 证明：
   - 由三角形三条边关系定则，$`c\left(C^\prime\right)\le C\left(C\right)`$；
   - 由c，$`c\left(H_G^\ast\right)\geq c\left(H_G^\ast-e\right)\geq c\left(T\right)`$；
   - 由d，$`c\left(C\right)=2\times c\left(T\right)`$；
   - 故$`c\left(C^\prime\right)\le2c\left(H_G^\ast\right)`$；即得证。 
   - 因此，该近似算法所得解不会最优解的2倍。


##### 近似比为1.5的算法（1.5-Approximation）


1. 构造最小生成树T（Minimum Spanning Tree）；
2. 分离在T上度数为奇数的点S（根据握手定理，S顶点数为偶数）；
3. 构造点集S在原完全图上的最小完美匹配M；
4. 将M和T的边集取并，构造多重图G（此时每个顶点均为偶数度）；
5. 生成G的欧拉回路（一笔画，符合无向图存在欧拉回路的充要条件）；
6. 选取捷径，跳过重复顶点（符合三角形三条边关系定则）。

- [ ] 🏠构建式启发/贪婪算法（Constructive heuristics）：主要是逐步插入点（边），最后得到一个包含所有城市的回路。

- [ ] 🌲克里斯托菲德斯算法（Christofides–Serdyukov algorithm）：可证明，最差情况下，该近似算法所得回路长度不会超过最优回路长度的1.5倍。

- [ ] 🦶基于“交换”的邻域优化算法（Random Swapping）：2-opt，3-opt，k-opt

- [ ] 🔥模拟“退火”的拟物优化算法（Simulated Annealing）：绝处逢生。

- [ ] 🐜模拟“蚁群”的拟物优化算法（Ant-Colony Optimization）：概率分布；距离+奖励值/信息素，超参数。


### proposed strategy 改进策略实现

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