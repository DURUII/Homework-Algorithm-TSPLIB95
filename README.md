# Traditional Algorithms for Symmetric Traveling Salesman Problem (TSP)

## benchmark 测试用例

⏱️海德堡大学（Heidelberg University）教授Gerhard
Reinelt维护的网站[TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)包含TSP问题的benchmark数据。

```commandline
gzip -d *.gz
```

🧮为EUC_2D类型且城市数小于等于1000的测试用例，共计48个。

## description 问题描述

🤯旅行商问题是一个典型的NP难度问题，可描述为平面上给定n个点，每两点之间的直线距离是已知的正实数，从某一个起点出发，经过其余点恰好一次，最后回到起点。要求给出一种巡回旅行走法，使得回路的长度最短。

1. 旅行商问题的类自然语言描述如下：给定$`n`$个城市，对这$`n`$个城市中的每两个城市来说，从一个城市到另一个城市所走的路程是已知的正实数，其中$`n`$是已知的正整数，$`n \ge 3`$。这$`n`$个城市的全排列共有$`n!`$的阶乘个。每一个这$`n`$个城市的全排列都恰好对应着一种走法：从全排列中的第一个城市走到第二个城市，……，从全排列中的第$`n-1`$个城市走到第$`n`$个城市，从全排列中的第$`n`$个城市回到第一个城市。要求给出一个这$`n`$个城市的全排列$`\sigma`$，使得在$`n!`$个全排列中，全排列$`\sigma`$对应的走法所走的路程是最短的。
> ▶️符合三角形三条边关系定则
> 
> ⬇️严格来讲，由于起点任意、顺逆时针等价，问题复杂度为$`\frac{\left(n-1\right)!}{2}`$

2. 旅行商问题的形式化描述：给定一个有向完全图$`G=\left(V,A\right)`$，其中集合$`V=v_1,\ldots,v_n`$是顶点集合，每个顶点代表一个城市，n是顶点数（$`n\ge 3`$），集合$`E=\left(v_i,v_j\right)|v_i,v_j\in V,v_i\neq v_j`$是有向边集合。 $`d_{ij}`$是有向边$`\left(v_i,v_j\right)`$的长度，$`d_{ij}`$是已知的正实数，其中$`\left(v_i,v_j\right)\in E`$。集合$`\Sigma`$是顶点全排列的集合，共有$`n!`$元素。$`\sigma`$是所有顶点的一个全排列，$`\sigma=\left(\sigma\left(1\right),\ldots,\sigma\left(n\right)\right)`$，$`\sigma\in\Sigma`$， $`\sigma\left(i\right)\in V`$，$`1\le i\ \le n`$。 $`\sigma`$对应着一条遍历所有顶点的回路：从顶点$`\sigma(1)`$走到顶点$`\sigma(2)`$，……，从顶点$`\sigma(n-1)`$走到顶点$`\sigma(n)`$，从顶点$`\sigma(n)`$回到顶点$`\sigma(1)`$。全排列$`\sigma`$所对应的回路的长度记为$`H(\sigma)`$，$`H(\sigma)=d_{\sigma(1) \sigma(2)} + ... + d_{\sigma(n-1) \sigma(n)} + d_{\sigma(n) \sigma(1)}`$。目标是给出所有顶点的一个全排列$`\sigma^*`$，使得$`H(\sigma^*)= \underset{\sigma \in \Sigma}{\min} (H(\sigma))`$。

> 🪞每一对顶点$`v_i`$ 和 $`v_j`$来说，都有$`d_{ij} = d_{ji}`$成立，那么称问题是对称的（Symmetric traveling salesman problem）； 否则称问题是非对称的（Asymmetric traveling salesman problem）。

## algorithm 演算法

🧄求解旅行商问题的算法设计可分为两类：完整算法和近似算法。

1. 完整算法保证给出最优解，但计算时间太长，仅可用于计算较小规模实例；
2. 近似算法，或许有可能在短时间内，给出相当接近最优解的近似解。非随机性近似算法包括构建式启发/贪婪算法，克里斯托菲德斯算法；随机性近似算法包括随机局域搜索、模拟退火、遗传算法、粒子群算法等。

🤖️*使用深度学习（Deep Learning）建模配合强化学习（Reinforcement learning）策略，`人工智能`，能不能与近70年来的`人类智能`相抗衡？一般认为：深度学习处理`模式识别/特征提取`比较好；深度学习求解`组合优化`问题，至今没有比较好的结果。不过，未来将至，未可知。

> The field of Combinatorial Optimization is pushing the limit of deep learning. Traditional solvers ***still*** provide better solutions than learning models. However, traditional solvers have been studied since the 1950s and the interest of applying deep learning to combinatorial optimization has just started. 
> 
> ——*The Transformer Network for the Traveling Salesman Problem*

> Specifically, taking the traveling salesman problem as the testbed problem, the performance of the solvers is assessed in five aspects, i.e., effectiveness, efficiency, stability, scalability, and generalization ability. Our results show that the solvers learned by NCO approaches, in general, ***still fall short*** of traditional solvers in nearly all these aspects. A potential benefit of NCO solvers would be their superior time and energy efficiency for small-size problem instances when sufficient training instances are available.  
> 
> —— *How Good Is Neural Combinatorial Optimization? A Systematic Evaluation on the Traveling Salesman Problem*

### fundamental 基石算法实现

#### 🏠构建式启发/贪婪算法（Constructive heuristics）

🍵主要是逐步插入点（边），最后得到一个包含所有城市的回路。例如：
+ 最近邻点算法：首先选择一个城市作为起点，然后用贪心法，每步均选择距离当前所在城市最近的未访问城市，最后回到起点。
+ 用贪心法选择符合要求的长度最短的边加入边集，直至边集构成一个哈密尔顿回路。要求如下：添加该边后，无法形成长度小于城市（顶点）数目的环，也无法形成“某城市（顶点）的度大于2”的格局。
+ “王磊”基本算法：首先生成一个3城市回路，然后依照一定次序，用贪心法将未访问城市插入回路，选择部分回路长度最短的动作，最后，得到包含所有城市的回路。

#### 🌲克里斯托菲德斯算法（Christofides–Serdyukov algorithm）

👍可证明，最差情况下，该近似算法所得回路长度不会超过最优回路长度的**1.5**倍。

> 🥁对于近似算法求最小值问题，设 $`Opt`$ 是最优解，$`x`$ 表示某算法给出的一个解，一般规定，$`Opt\le x\ \le\alpha\times Opt`$，$`\alpha`$记为该算法的近似比，作为评价算法优劣的指标之一。 
> 
> 🈚️拟物仿生万用启发算法（又称元启发算法，metaheuristic），虽然有可能得出比较好的近似解，但往往不涉及在最差情况下的效率证明。

✍️基于“最小生成树”的经典非随机性近似算法有两种，分别符合`2`和`1.5`的近似比。

##### 近似比为2的算法（2-Approximation）

1. 定义：$`S`$代表一系列边（允许重边），$`c\left(S\right)`$代表各边权重（长度）之和。
2. 定义：$`H_G^\ast`$为无向多重图$`G`$上，长度最短的哈密尔顿回路（Hamiltonian Cycle），途中经过所有点且只经过一次。
3. 构造最小生成树$`T`$，根据最小权生成树定义，$`c\left(H_G^\ast\right)\geq c\left(H_G^\ast-e\right)\geq c\left(T\right)`$。 

![](/assets/images/mst-1.png)

4. 按深度优先搜索次序记录回路$`C`$，下探一次，回溯一次，因此$`c\left(C\right)=2\times c\left(T\right)`$。例如，1，2，3，2，4，2，1，5，1，6......1。 
5. 搭桥（short-cut/bypass）略过重复访问的点得到符合问题描述的新回路$`C^\prime`$（最后回到起点），例如，1，2，3，4，5，6......1。 

> 问题要求商人巡回旅行最后回到起点，省略号前是$`1~n`$的一个排列。

![](/assets/images/mst-2.png)

6. 证明：
   - 由e、三角形三条边关系定则，$`c\left(C^\prime\right)\le c\left(C\right)`$；
   - 由c，$`c\left(H_G^\ast\right)\geq c\left(H_G^\ast-e\right)\geq c\left(T\right)`$；
   - 由d，$`c\left(C\right)=2\times c\left(T\right)`$；
   - 故$`c\left(C^\prime\right)\le2c\left(H_G^\ast\right)`$；即得证。 
   - 因此，该近似算法所得解，最多也不会超过最优解的2倍。

##### 近似比为1.5的算法（1.5-Approximation）

> 仍基于最小生成树，想方设法减小“每边下探一次，回溯一次”带来的额外开销。
> 
> `一笔画`、`不重边`地遍历所有顶点，可以将问题转换成`欧拉回路`问题。无向图存在欧拉回路的充要条件为：该图为连通图，且所有顶点度数均为偶数。
> 
> 倘若`奇度数`顶点为偶数个（证明见下），那么可以通过将其***两两匹配***，为每一个顶点都`附赠`一个度，这样便可以满足`顶点度数均为偶数`条件。

1. 定义：$`S`$代表一系列边（允许重边），$`c\left(S\right)`$代表各边权重（长度）之和。
2. 定义：$`H_G^\ast`$为无向多重图$`G`$上，长度最短的哈密尔顿回路（Hamiltonian Cycle），即途中经过所有点且只经过一次。
3. 定义：假设$`S`$为无向多重图$`G`$上的导出子图，在$`S`$上长度最短的哈密尔顿回路记为$`H_S^\ast`$。根据三角形三边关系定则易证，$`c\left(H_S^\ast\right)\le c\left(H_G^\ast\right)`$。
4. 构造最小生成树$`T`$，根据最小权生成树定义，$`c\left(H_G^\ast\right)\geq c\left(H_G^\ast-e\right)\geq c\left(T\right)`$。
5. 分离在$`T`$上度数为奇数的点，生成导出子图$`S`$（根据握手定理，给定无向图$`G=\left(V,E\right)`$，一条边贡献2度，故有$`\Sigma degG\left(v\right)=2\left|E\right|`$；除开度数为偶数的顶点所贡献的度数，推论可知，度数为奇数顶点数有偶数个）；
6. 构造$`S`$的最小权完美匹配$`M`$，构造多重图$`G^\prime=T\ \cup M`$（此时每个顶点均为偶数度，故存在欧拉回路）；

![](assets/images/Euler.png)

7. 生成$`G^\prime`$的欧拉回路$`C`$，$`c\left(C\right)=c\left(T\right)+c\left(M\right)`$;
8. 搭桥（short-cut/bypass）略过重复访问的点（起点终点不删）得到符合问题描述的新回路$`C^\prime`$（最后回到起点）。
9. 证明：
	- 由e、三角形三边关系定则，$`c\left(C^\prime\right)\le c\left(C\right)`$；
	- 由d，$`c\left(H_G^\ast\right)\geq c\left(H_G^\ast-e\right)\geq c\left(T\right)`$；
	- 由g，$`c\left(C\right)=c\left(T\right)+c\left(M\right)`$；
    - 由f、c，$`c\left(M\right)+c\left(M\right)\le c\left(M1\right)+c\left(M2\right)=c\left(H_S^\ast\right)\le c\left(H_G^\ast\right)`$。
    - 故$`c\left(C^\prime\right)\le c\left(T\right)+c\left(M\right)\le c\left(H_G^\ast\right)+\frac{1}{2}c\left(H_G^\ast\right)`$；即得证。

![](assets/images/match.png)

#### 基于邻域跳坑的（元）启发算法

##### 邻域结构
解空间中的一个巡回旅行路线直接或间接对应一个全排列$`\sigma=\left(\sigma\left(1\right),\ldots,\sigma\left(n\right)\right)）`$。将其视作$`n`$维空间中的一个点，其邻域常常定义为$`\sigma`$对换和移动后转化成的$`\sigma^\prime`$。此外Cores提出的2-opt扰动也很经典。

![](assets/images/opt-2.png)

##### 跳坑思想
处理TSP问题的常见思路之一是：先使用非随机性启发算法获得一个相对合理的解，再进行后处理，使用万用启发式算法跳出局部最优，以期待结果有所提升。这仿佛王磊老师经常说的，“如果你期末总评已经满绩了，就要见贤思齐，到更有希望的区域继续提高。”

不过，**_“大智”常常“若愚”，“峰回”方有“路转”，谁说“错棋”不能“封神”，谁说“绝处”不能“逢生”_**；如果一个人时时刻刻都太精明，反而让人生烦，不利于开展工作。因此，我认为，更为精明的跳槽策略，企业家的儿子先苦心志、劳筋骨，先去稍微比董事长低一点的职位试试水，甚至瞎猫碰上死耗子，跌跌撞撞直接去基层工作也不是不可，带着民间智慧总能回来继承家业，发扬光大的。也就是说：
- 若新位置明显优于旧位置，则跳转至新位置；
- 纵使新的位置不如旧位置，也要以“一定概率”跳转至新位置。

##### 模拟退火 
事实上，人们从物理世界状态演化、自然界各种现象、千百年来生存斗争经验获得启发，以仿生拟人拟物途径设计了各种千奇百怪五花八门的算法。即使有学者认为如此依赖一个通用一成不变因而往往不贴切的物理世界并不贴切，应当向比晶体有更高智慧的人学习；不可否认，模拟退火（Simulated Annealing）具有思想根源和自然背景。因此，本次课程作业没有逃避使用此算法。

模拟退火的超参数包括：初始温度、终止温度、指数衰减系数、运行时间。

模拟退火的通用步骤是：
1. 在解空间选择一个初始格局$`\sigma`$； 
2. 温度以一定系数衰减，若小于终止温度，算法停机；否则，循环执行c；
3. 邻域搜索：在当前格局的周围（随机点边对换等）找一个邻近格局$`\sigma^\prime`$，根据度量指标计算优劣$`\Delta E=E\left(\sigma^\prime\right)-E\left(\sigma\right)`$（E越小越好），跳坑策略：
   - 如果$`\Delta E\ <0`$，则直接令$`\sigma=\sigma^\prime`$；
   - 如果$`\Delta E\ \geq0`$，以$`e^{-\frac{\Delta E}{T}}`$的概率，令$`\sigma=\sigma^\prime`$。

上述通用步骤重置启动，若干次。


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
6. [AcWing算法进阶课 - 模拟退火](https://www.acwing.com/activity/content/32/)
7. [Prof.Bresson - Learning to Solve the Traveling Salesman Problem](https://www.bilibili.com/video/BV13R4y1W7sh/)
8. [维基百科 - Travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem)