from py2neo import Graph, Node, Relationship
from config import graph
with open("../raw_data/relation.txt", encoding="utf-8") as f:
    for line in f.readlines():
        rela_array = line.strip("\n").split(",")
        print(rela_array)

        # 使用 MERGE 创建或匹配节点
        graph.run("MERGE (p:Person {cate: $cate, Name: $name})", cate=rela_array[3], name=rela_array[0])
        graph.run("MERGE (p:Person {cate: $cate, Name: $name})", cate=rela_array[4], name=rela_array[1])

        # 使用 MATCH 查找节点并创建关系
        graph.run(
            "MATCH (e:Person), (cc:Person) "
            "WHERE e.Name = $name1 AND cc.Name = $name2 "
            "MERGE (e)-[r:%s {relation: $relation}]->(cc) "
            "RETURN r" % rela_array[2],
            name1=rela_array[0], name2=rela_array[1], relation=rela_array[2]
        )
