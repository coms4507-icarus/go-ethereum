package icarus

import "sync"

// Mike's code
type ThreadSafeGraph struct {
	graph map[string][]string
	*sync.RWMutex
}

func newThreadSafeGraph() *ThreadSafeGraph {
	return &ThreadSafeGraph{graph: make(map[string][]string)}
}

// End Mike's code
