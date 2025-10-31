#!/usr/bin/env python3
"""
Script to run research on Coca Cola and Apple Macintosh commercials from the 1980s.
"""

import sys
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
load_dotenv()
# Add the Research directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Research'))

from research_agent import researcher_agent

def main():
    research_topic = "Air jordan 1 commercials"
    
    print(f"[SEARCH] Starting research on: {research_topic}")
    print("=" * 80)
    
    try:
        # Properly structure the input for the research agent
        initial_state = {
            "researcher_messages": [
                HumanMessage(content=research_topic)
            ],
            "tool_call_iterations": 0,
            "research_topic": research_topic,
            "compressed_research": "",
            "raw_notes": []
        }
        
        # Run the research
        print("[START] Invoking research agent...")
        result = researcher_agent.invoke(initial_state)
        
        print("\n[OK] RESEARCH COMPLETED!")
        print("=" * 80)
        
        # Prepare output directory and file path
        from datetime import datetime
        import pathlib
        base_dir = pathlib.Path(os.path.dirname(__file__)).parent
        outputs_dir = base_dir / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() or c in ("-", "_", " ") else "_" for c in research_topic).strip().replace(" ", "_")
        output_file = outputs_dir / f"research_{safe_topic}_{timestamp}.md"

        print("\n COMPRESSED RESEARCH FINDINGS:")
        print("-" * 50)
        compressed = result.get('compressed_research', 'No compressed research available')
        print(compressed)
        
        print(f"\n[WRITE] RAW RESEARCH NOTES ({len(result.get('raw_notes', []))} notes):")
        print("-" * 50)
        raw_notes = result.get('raw_notes', [])
        if raw_notes:
            for i, note in enumerate(raw_notes, 1):
                print(f"\n--- Raw Note {i} ---")
                print(note[:500] + "..." if len(note) > 500 else note)
        else:
            print("No raw notes available")
            
        print(f"\n RESEARCHER MESSAGES ({len(result.get('researcher_messages', []))} messages):")
        print("-" * 50)
        messages = result.get('researcher_messages', [])
        for i, msg in enumerate(messages, 1):
            msg_type = type(msg).__name__
            content_preview = str(msg.content)[:200] + "..." if len(str(msg.content)) > 200 else str(msg.content)
            print(f"\n{i}. {msg_type}: {content_preview}")
        
        # Write full output to file (markdown)
        report_lines = []
        report_lines.append(f"# Research Report: {research_topic}\n")
        report_lines.append(f"Generated: {timestamp}\n")
        report_lines.append("\n## Compressed Research Findings\n")
        report_lines.append(compressed if isinstance(compressed, str) else str(compressed))
        report_lines.append("\n\n## Raw Research Notes\n")
        if raw_notes:
            for i, note in enumerate(raw_notes, 1):
                report_lines.append(f"\n### Note {i}\n")
                report_lines.append(note if isinstance(note, str) else str(note))
        else:
            report_lines.append("No raw notes available")
        report_lines.append("\n\n## Researcher Messages (Preview)\n")
        if messages:
            for i, msg in enumerate(messages, 1):
                msg_type = type(msg).__name__
                content_text = str(msg.content)
                preview = content_text[:200] + ("..." if len(content_text) > 200 else "")
                report_lines.append(f"- {i}. {msg_type}: {preview}")
        else:
            report_lines.append("No messages available")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        print(f"\n Results written to: {output_file}")
        
        print("\n[OK] Research process completed successfully!")
        
    except Exception as e:
        print(f"[ERROR] Error during research: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
