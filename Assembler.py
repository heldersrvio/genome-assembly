class DoubleLinkedList:
	def __init__(self):
		self.count = 0
		self.firstElement = None
	def insert(self, element):
		if self.count == 0:
			element.next = element
			element.previous = element
			self.firstElement = element
		else:
			element.next = self.firstElement
			element.previous = self.firstElement.previous
			self.firstElement.previous.next = element
			self.firstElement.previous = element
		self.count += 1
		return element
	def insertAfter(self, insertedElement, previousElement):
		insertedElement.next = previousElement.next
		insertedElement.previous = previousElement
		previousElement.next.previous = insertedElement
		previousElement.next = insertedElement
		self.count += 1
		return insertedElement
	def insertBefore(self, insertedElement, nextElement):
		insertedElement.next = nextElement
		insertedElement.previous = nextElement.previous
		nextElement.previous.next = insertedElement
		nextElement.previous = insertedElement
		self.count += 1
		return insertedElement
	def remove(self, element):
		element.previous.next = element.next
		element.next.previous = element.previous
		if self.firstElement == element and self.count > 1:
			self.firstElement = element.previous
		elif self.firstElement == element:
			self.firstElement = None
		self.count -= 1
		return element

class AVLTreeNode:
	def __init__(self, graphNode):
		self.graphNode = graphNode
		self.left = None
		self.right = None
		self.height = 1

class AVLTree:
	def __init__(self):
		self.mostRecentNode = None
	def insert(self, root, name1, name2):
		if root is None:
			self.mostRecentNode = AVLTreeNode(GraphNode(name1, name2))
			return self.mostRecentNode
		elif name1 + name2 < root.graphNode.name1 + root.graphNode.name2:
			root.left = self.insert(root.left, name1, name2)
		elif name1 + name2 > root.graphNode.name1 + root.graphNode.name2:
			root.right = self.insert(root.right, name1, name2)
		else:
			self.mostRecentNode = root
			return root
		root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
		balance = self.getBalance(root)
		if balance > 1 and name1 + name2 < root.left.graphNode.name1 + root.left.graphNode.name2:
			return self.rightRotate(root)
		if balance < -1 and name1 + name2 > root.right.graphNode.name1 + root.right.graphNode.name2:
			return self.leftRotate(root)
		if balance > 1 and name1 + name2 > root.left.graphNode.name1 + root.left.graphNode.name2:
			root.left = self.leftRotate(root.left)
			return self.rightRotate(root)
		if balance < -1 and name1 + name2 < root.right.graphNode.name1 + root.right.graphNode.name2:
			root.right = self.rightRotate(root.right)
			return self.leftRotate(root)
		return root
	def leftRotate(self, oldRoot):
		newRoot = oldRoot.right
		t2 = newRoot.left
		newRoot.left = oldRoot
		oldRoot.right = t2
		oldRoot.height = 1 + max(self.getHeight(oldRoot.left), self.getHeight(oldRoot.right))
		newRoot.height = 1 + max(self.getHeight(newRoot.left), self.getHeight(newRoot.right))
		return newRoot
	def rightRotate(self, oldRoot):
		newRoot = oldRoot.left
		t3 = newRoot.right
		newRoot.right = oldRoot
		oldRoot.left = t3
		oldRoot.height = 1 + max(self.getHeight(oldRoot.left), self.getHeight(oldRoot.right))
		newRoot.height = 1 + max(self.getHeight(newRoot.left), self.getHeight(newRoot.right))
		return newRoot
	def getHeight(self, root):
		if root is None:
			return 0
		return root.height
	def getBalance(self, root):
		if root is None:
			return 0
		return self.getHeight(root.left) - self.getHeight(root.right)

class GraphNode:
	def __init__(self, name1, name2):
		self.name1 = name1
		self.name2 = name2
		self.hasPrevious = False
		self.edges = []
	def connectToNode(self, edge):
		self.edges.append(edge)

class GraphEdge:
	def __init__(self, graph, pattern1, pattern2):
		self.pattern1 = pattern1
		self.pattern2 = pattern2
		originNode = graph.addNode(pattern1[: len(pattern1) - 1], pattern2[: len(pattern2) - 1])
		if not originNode.hasPrevious:
			graph.firstNodeCandidates.append(originNode)
		self.endNode = graph.addNode(pattern1[1:], pattern2[1:])
		if self.endNode in graph.firstNodeCandidates:
			graph.firstNodeCandidates.remove(self.endNode)
		if self.endNode == graph.firstNode or graph.firstNode is None:
			graph.firstNode = graph.firstNodeCandidates[0]
		self.endNode.hasPrevious = True
		originNode.connectToNode(self)
		graph.edgeCount += 1

class Graph:
	def __init__(self):
		self.nodeTree = AVLTree()
		self.nodeTreeRoot = None
		self.firstNode = None
		self.edgeCount = 0
		self.firstNodeCandidates = []
	def addNode(self, name1, name2):
		self.nodeTreeRoot = self.nodeTree.insert(self.nodeTreeRoot, name1, name2)
		return self.nodeTree.mostRecentNode.graphNode
	def createEdge(self, pattern1, pattern2):
		GraphEdge(self, pattern1, pattern2)
	def HierholzerFindEulerianPath(self):
		path = DoubleLinkedList()
		nextCycleCandidates = DoubleLinkedList()
		if self.firstNode is None:
			return path
		currentNode = self.firstNode
		reachedEnd = False
		while len(currentNode.edges) > 0 or nextCycleCandidates.count > 0:
			if not hasattr(currentNode, "unvisitedEdges"):
				nextCycleCandidates.insert(currentNode)
				currentNode.unvisitedEdges = []
				for edge in currentNode.edges:
					currentNode.unvisitedEdges.append(edge)
			if len(currentNode.unvisitedEdges) > 0:
				if hasattr(currentNode, "lastEdgeAddedToPath") and reachedEnd:
					path.insertBefore(currentNode.unvisitedEdges[0], currentNode.lastEdgeAddedToPath)
				else:
					path.insert(currentNode.unvisitedEdges[0])
				if len(currentNode.unvisitedEdges) < 2:
					nextCycleCandidates.remove(currentNode)
				currentNode.lastEdgeAddedToPath = currentNode.unvisitedEdges[0]
				currentNode = currentNode.unvisitedEdges.pop(0).endNode
			else:
				if len(currentNode.edges) == 0:
					reachedEnd = True
				if nextCycleCandidates.firstElement == currentNode:
					nextCycleCandidates.remove(currentNode)
				currentNode = nextCycleCandidates.firstElement
		return path
	def getSequence(self):
		path = self.HierholzerFindEulerianPath()

		sequence = ""
		k = len(path.firstElement.pattern1)
		currentPrefixEdge = path.firstElement
		currentSuffixEdge = path.firstElement
		sequence += currentPrefixEdge.pattern1
		currentPrefixEdge = currentPrefixEdge.next
		i = 0
		while currentPrefixEdge != path.firstElement:
			i += 1
			if currentSuffixEdge.pattern2 == currentPrefixEdge.pattern1:
				currentSuffixEdge = currentSuffixEdge.next
			else:
				currentSuffixEdge = path.firstElement
			sequence += currentPrefixEdge.pattern1[k - 1]
			currentPrefixEdge = currentPrefixEdge.next
		while currentSuffixEdge != path.firstElement:
			sequence += currentSuffixEdge.pattern2[k - 1]
			currentSuffixEdge = currentSuffixEdge.next
		return sequence

def createGraphFromInput():
	nucleotides = ["A", "T", "U", "C", "G"]
	input = open("output.txt", "r")
	graph = Graph()
	for line in input:
		pattern1 = ""
		pattern2 = ""
		pattern1Done = False
		for character in line:
			if character == "|":
				pattern1Done = True
			elif not pattern1Done and character in nucleotides:
				pattern1 += character
			elif character in nucleotides:
				pattern2 += character
		graph.createEdge(pattern1, pattern2)
	input.close()
	return graph

def getSequence():
	return createGraphFromInput().getSequence()	

def saveResults():
	output = open("output.fasta", "w")
	output.write(getSequence())

saveResults()
