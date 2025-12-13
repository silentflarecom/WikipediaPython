<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as d3 from 'd3'
import axios from 'axios'

const props = defineProps({
  taskId: {
    type: Number,
    required: true
  }
})

const container = ref(null)
const loading = ref(false)
const graphData = ref({ nodes: [], edges: [] })
let simulation = null

const fetchGraphData = async () => {
  if (!props.taskId) return
  loading.value = true
  try {
    const response = await axios.get(`http://localhost:8000/api/batch/${props.taskId}/graph`)
    graphData.value = response.data
    renderGraph()
  } catch (e) {
    console.error("Error fetching graph:", e)
  } finally {
    loading.value = false
  }
}

const renderGraph = () => {
  if (!container.value || !graphData.value.nodes.length) return

  // Clear previous SVG
  d3.select(container.value).selectAll("*").remove()

  const width = container.value.clientWidth
  const height = 600
  
  const svg = d3.select(container.value)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "max-width: 100%; height: auto;")

  // Simulation setup
  simulation = d3.forceSimulation(graphData.value.nodes)
    .force("link", d3.forceLink(graphData.value.edges).id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collide", d3.forceCollide(30))

  // Render links
  const link = svg.append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(graphData.value.edges)
    .join("line")
    .attr("stroke-width", d => Math.sqrt(d.value || 1))

  // Render nodes
  const node = svg.append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(graphData.value.nodes)
    .join("circle")
    .attr("r", d => d.status === 'completed' ? 8 : 5)
    .attr("fill", d => {
        // Color by depth
        const colors = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b"]
        return colors[d.depth % colors.length] || "#888"
    })
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended))

  node.append("title")
    .text(d => d.label)
    
  // Labels
  const labels = svg.append("g")
    .attr("class", "labels")
    .selectAll("text")
    .data(graphData.value.nodes)
    .enter()
    .append("text")
    .attr("dx", 12)
    .attr("dy", ".35em")
    .text(d => d.label)
    .style("font-size", "10px")
    .style("pointer-events", "none")
    .style("fill", "#333")

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y)

    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y)
      
    labels
      .attr("x", d => d.x)
      .attr("y", d => d.y)
  })

  // Zoom behavior
  const zoom = d3.zoom()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => {
          svg.selectAll("g").attr("transform", event.transform);
      });
      
  svg.call(zoom);

  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart()
    event.subject.fx = event.subject.x
    event.subject.fy = event.subject.y
  }

  function dragged(event) {
    event.subject.fx = event.x
    event.subject.fy = event.y
  }

  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0)
    event.subject.fx = null
    event.subject.fy = null
  }
}

watch(() => props.taskId, () => {
  fetchGraphData()
})

onMounted(() => {
  fetchGraphData()
})

onUnmounted(() => {
  if (simulation) simulation.stop()
})
</script>

<template>
  <div class="border rounded-lg bg-white p-4 shadow-sm">
    <div class="flex justify-between items-center mb-4 border-b pb-2">
        <h3 class="font-bold text-gray-700">Knowledge Graph</h3>
        <button @click="fetchGraphData" class="text-sm text-blue-600 hover:text-blue-800">
            Refresh
        </button>
    </div>
    
    <div v-if="loading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
    
    <div ref="container" class="w-full h-[600px] bg-gray-50 rounded overflow-hidden relative">
      <div v-if="!loading && graphData.nodes.length === 0" class="absolute inset-0 flex items-center justify-center text-gray-400">
        No graph data available
      </div>
    </div>
    
    <div class="mt-2 flex gap-4 text-xs text-gray-600">
        <div class="flex items-center gap-1">
            <span class="w-3 h-3 rounded-full bg-red-500 block"></span> Depth 0 (Root)
        </div>
        <div class="flex items-center gap-1">
            <span class="w-3 h-3 rounded-full bg-blue-500 block"></span> Depth 1
        </div>
        <div class="flex items-center gap-1">
            <span class="w-3 h-3 rounded-full bg-green-500 block"></span> Depth 2
        </div>
    </div>
  </div>
</template>
