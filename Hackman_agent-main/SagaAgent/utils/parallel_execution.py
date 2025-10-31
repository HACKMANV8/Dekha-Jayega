"""
Parallel Saga Generation Execution
Provides utilities for running independent nodes in parallel for faster generation
"""

import asyncio
import time
import warnings
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List, Callable
from collections import defaultdict

# Suppress Pydantic warnings about additionalProperties (common with Gemini models)
warnings.filterwarnings("ignore", message=".*additionalProperties.*")


class PerformanceMonitor:
    """Track performance metrics for parallel execution"""
    
    def __init__(self):
        self.timings = defaultdict(list)
        self.enabled = True
    
    def track(self, stage: str):
        """Context manager for tracking stage timing"""
        return StageTimer(self, stage)
    
    def report(self):
        """Print performance report"""
        if not self.timings:
            return
            
        print("\n" + "="*70)
        print("[STATS] PERFORMANCE REPORT")
        print("="*70)
        
        for stage, times in self.timings.items():
            avg_time = sum(times) / len(times)
            print(f"{stage:20s}: {avg_time:.2f}s (n={len(times)})")
        
        total = sum(sum(times) for times in self.timings.values())
        print(f"{'TOTAL':20s}: {total:.2f}s ({total/60:.1f} minutes)")
        print("="*70)


class StageTimer:
    """Context manager for timing stages"""
    
    def __init__(self, monitor: PerformanceMonitor, stage: str):
        self.monitor = monitor
        self.stage = stage
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        elapsed = time.time() - self.start_time
        self.monitor.timings[self.stage].append(elapsed)


class ParallelExecutor:
    """Execute saga generation nodes in parallel"""
    
    def __init__(self, max_workers: int = 3, retry_sequential: bool = True):
        """
        Args:
            max_workers: Maximum number of parallel workers
            retry_sequential: If True, fallback to sequential on error
        """
        self.max_workers = max_workers
        self.retry_sequential = retry_sequential
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.monitor = PerformanceMonitor()
    
    async def run_in_executor(self, func: Callable, *args) -> Any:
        """Run synchronous function in executor"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, func, *args)
    
    async def parallel_level_1(self, state: Dict[str, Any], nodes: Dict[str, Callable]) -> Dict[str, Any]:
        """
        Run Level 1 nodes in parallel (e.g., world_lore, factions, characters)
        These can all run simultaneously after concept is complete
        
        Args:
            state: Current saga state
            nodes: Dictionary of {node_name: node_function}
        
        Returns:
            Merged state from all parallel nodes
        """
        print("\n" + "="*70)
        print("[PARALLEL] PARALLEL EXECUTION - Level 1")
        node_names = ", ".join(nodes.keys())
        print(f"   Running: {node_names}")
        print("="*70)
        
        with self.monitor.track("parallel_batch"):
            # Create tasks for parallel execution
            tasks = []
            node_list = []
            
            for node_name, node_func in nodes.items():
                print(f"    Preparing {node_name}...")
                task = self.run_in_executor(node_func, state)
                tasks.append(task)
                node_list.append(node_name)
            
            # Run all in parallel and gather results
            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)
            except Exception as e:
                print(f"[ERROR] Parallel execution failed during gather: {e}")
                if self.retry_sequential:
                    return await self._fallback_sequential(state, nodes)
                raise
            
            # Merge results
            merged_state = {}
            errors = []
            
            for i, result in enumerate(results):
                node_name = node_list[i]
                if isinstance(result, Exception):
                    errors.append((node_name, result))
                    print(f"[ERROR] {node_name} failed with exception: {str(result)[:100]}")
                elif isinstance(result, dict):
                    # Log what keys were returned
                    result_keys = list(result.keys()) if result else []
                    print(f"[OK] {node_name} completed - returned keys: {result_keys}")
                    
                    # Check if result is empty
                    if not result:
                        print(f"WARNING: {node_name} returned empty dict")
                    
                    merged_state.update(result)
                elif result is None:
                    print(f"WARNING: {node_name} returned None")
                else:
                    print(f"WARNING: {node_name} returned unexpected type: {type(result)}")
            
            # Only fallback if ALL tasks failed or if there were critical errors
            if errors:
                if len(errors) == len(nodes):
                    print(f"[ERROR] All {len(errors)} task(s) failed, falling back to sequential")
                    if self.retry_sequential:
                        return await self._fallback_sequential(state, nodes)
                else:
                    print(f"WARNING: {len(errors)} of {len(nodes)} task(s) failed, continuing with partial results")
                    # Continue with partial results from successful tasks
        
        return merged_state
    
    async def _fallback_sequential(self, state: Dict[str, Any], nodes: Dict[str, Callable]) -> Dict[str, Any]:
        """Fallback to sequential execution on error"""
        print("\nWARNING: Falling back to sequential execution...")
        
        merged_state = {}
        for node_name, node_func in nodes.items():
            try:
                print(f"   Running {node_name}...")
                result = await self.run_in_executor(node_func, state)
                if isinstance(result, dict):
                    merged_state.update(result)
                    # Update state for next node
                    state = {**state, **merged_state}
                    print(f"   [OK] {node_name} completed")
            except Exception as e:
                print(f"   [ERROR] {node_name} failed: {e}")
                # Continue with other nodes
        
        return merged_state
    
    def close(self):
        """Clean up executor"""
        self.executor.shutdown(wait=True)
    
    def get_report(self):
        """Get performance report"""
        self.monitor.report()


async def generate_saga_parallel(
    state: Dict[str, Any],
    concept_func: Callable,
    parallel_nodes: Dict[str, Callable],
    plot_func: Callable,
    quest_func: Callable,
    max_workers: int = 3,
    retry_sequential: bool = True
) -> Dict[str, Any]:
    """
    Generate saga with parallel execution
    
    Flow:
    1. Concept (sequential)
    2. [World Lore || Factions || Characters] (parallel)
    3. Plot Arcs (sequential, needs world context)
    4. Questlines (sequential, needs plot)
    
    Args:
        state: Initial saga state
        concept_func: Concept generation function
        parallel_nodes: Dict of parallel node functions {name: func}
        plot_func: Plot generation function
        quest_func: Quest generation function
        max_workers: Maximum parallel workers
        retry_sequential: Fallback to sequential on error
    
    Returns:
        Final saga state
    """
    print("\n" + "="*70)
    print("[START] PARALLEL SAGA GENERATION")
    print("="*70)
    
    executor = ParallelExecutor(max_workers=max_workers, retry_sequential=retry_sequential)
    
    try:
        # Stage 1: Concept (must be sequential)
        print("\n[CONCEPT] Stage 1: Creating Concept...")
        with executor.monitor.track("concept"):
            concept_result = await executor.run_in_executor(concept_func, state)
            if concept_result:
                state.update(concept_result)
                concept = state.get('concept', {})
                title = concept.get('title', 'N/A') if isinstance(concept, dict) else 'N/A'
                print(f"[OK] Concept generated: title='{title}'")
            else:
                print("[ERROR] Concept generation returned empty result")
                raise ValueError("Concept generation failed - no result returned")
        
        # Verify concept is in state before continuing
        if not state.get("concept"):
            print("[ERROR] Concept is missing from state")
            raise ValueError("Concept is required but missing from state")
        
        # Stage 2: Parallel execution (world_lore, factions, characters)
        print("\n[PARALLEL] Stage 2: Parallel Batch (World Lore, Factions, Characters)")
        print(f"[STATS] State before parallel execution:")
        print(f"   - topic: {state.get('topic', 'N/A')[:50]}...")
        concept = state.get('concept', {})
        print(f"   - concept title: {concept.get('title', 'N/A') if isinstance(concept, dict) else 'N/A'}")
        
        parallel_result = await executor.parallel_level_1(state, parallel_nodes)
        if parallel_result:
            state.update(parallel_result)
        else:
            print("WARNING: Parallel execution returned empty result")
        
        # Verify parallel results
        print(f"\n[STATS] State after parallel execution:")
        print(f"   - world_lore: {'present' if state.get('world_lore') else 'missing'}")
        print(f"   - factions: {len(state.get('factions', []))} generated")
        print(f"   - characters: {len(state.get('characters', []))} generated")
        
        # Stage 3: Plot Arcs (needs world context)
        print("\n[PLOT] Stage 3: Creating Plot Arcs...")
        if not state.get("world_lore"):
            print("WARNING: No world lore in state, plots may be generic")
        
        with executor.monitor.track("plot_arcs"):
            plot_result = await executor.run_in_executor(plot_func, state)
            if plot_result:
                state.update(plot_result)
                print(f"[OK] Plot arcs generated: {len(state.get('plot_arcs', []))} arcs")
            else:
                print("WARNING: Plot generation returned empty result")
        
        # Stage 4: Questlines (needs plot)
        print("\n[QUEST] Stage 4: Creating Questlines...")
        with executor.monitor.track("questlines"):
            quest_result = await executor.run_in_executor(quest_func, state)
            if quest_result:
                state.update(quest_result)
                print(f"[OK] Questlines generated: {len(state.get('questlines', []))} quests")
            else:
                print("WARNING: Quest generation returned empty result")
        
        # Show performance report
        executor.get_report()
        
        print("\n" + "="*70)
        print("[OK] PARALLEL SAGA GENERATION COMPLETE")
        print("="*70)
        
        return state
    
    finally:
        executor.close()


def run_parallel_generation(
    state: Dict[str, Any],
    concept_func: Callable,
    parallel_nodes: Dict[str, Callable],
    plot_func: Callable,
    quest_func: Callable,
    max_workers: int = 3,
    retry_sequential: bool = True
) -> Dict[str, Any]:
    """Synchronous wrapper for parallel generation"""
    return asyncio.run(
        generate_saga_parallel(
            state=state,
            concept_func=concept_func,
            parallel_nodes=parallel_nodes,
            plot_func=plot_func,
            quest_func=quest_func,
            max_workers=max_workers,
            retry_sequential=retry_sequential
        )
    )

