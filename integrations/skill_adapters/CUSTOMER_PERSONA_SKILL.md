# Customer Persona Identification Skill

## Overview

The **customer-persona-identification** skill enables the ByteBastDev framework to identify, segment, and prioritize customer personas based on business data, market analysis, and customer evidence (CRM, interviews, analytics, etc.).

## Capabilities

This skill provides the following capabilities:

### Core Functionality
- **identify_personas**: Generate actionable customer persona cards from business data
- **segment_customers**: Segment customers based on characteristics and behaviors
- **jobs_to_be_done_analysis**: Analyze customer jobs-to-be-done (JTBD)
- **pain_gain_mapping**: Map customer pains and gains
- **message_map_creation**: Create messaging frameworks for personas
- **objection_handling**: Identify objections and develop reassurances
- **channel_prioritization**: Prioritize marketing channels for each persona
- **icp_scoring**: Create ICP (Ideal Customer Profile) scorecards
- **persona_prioritization**: Prioritize personas by impact, fit, and access
- **intent_signal_identification**: Identify purchase intent signals

## Input Parameters

When using this skill, you can provide the following inputs:

```python
{
    "company_overview": "Company context, value proposition, differentiation",
    "products_services": [
        {
            "name": "Product Name",
            "price": 99,
            "description": "Product description"
        }
    ],
    "target_markets": ["B2B SaaS", "Enterprise", "North America"],
    "evidence_sources": {
        "crm_data": "path/to/crm.csv",
        "interviews": ["Interview notes..."],
        "analytics": {"monthly_users": 5000}
    },
    "constraints": {
        "compliance": ["GDPR"],
        "budget": 50000,
        "channels": ["LinkedIn", "Email"]
    },
    "strategic_goals": {
        "target_arr": 1000000,
        "target_cac": 500,
        "target_ltv": 5000
    },
    "max_personas": 6
}
```

## Output Format

The skill generates a structured JSON output with:

### Personas
Each persona includes:
- **Identity**: Label, type (B2B/B2C), role/archetype
- **Company Profile** (for B2B): Industry, size, geography
- **Jobs-to-be-Done**: Structured JTBD statements
- **Pains & Gains**: Customer pain points and desired outcomes
- **Purchase Triggers**: What initiates buying process
- **Decision Criteria**: How they evaluate solutions
- **Objections**: Common objections and reassurances
- **Channels**: Preferred marketing channels and formats
- **Message Map**: Core promise, proof points, CTAs, angles
- **Offers & Pricing Hooks**: Relevant offer structures
- **Intent Signals**: What indicates readiness to buy
- **Priority Scores**: Impact, fit, access scores (0-5 each)

### Gap Analysis
- List of missing data that would improve persona quality
- Recommended data sources to collect

### Next Steps
- Actionable recommendations for validation and implementation
- Suggested tests and campaigns

## Example Usage

### Via Framework CLI

```bash
python orchestrator/main.py --task "Identify buyer personas for our B2B SaaS platform targeting marketing teams"
```

### Via Python API

```python
from integrations.skill_adapters import MarketingSkillsAdapter
import asyncio

# Initialize adapter
adapter = MarketingSkillsAdapter({
    'skills_path': '/mnt/skills',
    'output_dir': './output'
})

# Execute persona identification
result = asyncio.run(adapter.identify_customer_personas(
    company_overview="We provide AI-powered content creation tools for marketing teams",
    products_services=[
        {"name": "Pro Plan", "price": 99, "arpu": 99}
    ],
    target_markets=["B2B SaaS", "Marketing teams", "50-500 employees"],
    strategic_goals={
        "target_arr": 1000000,
        "target_cac": 500
    }
))

print(f"Generated {result['summary']['total_personas']} personas")
```

## Keywords That Trigger This Skill

The task planner automatically detects when this skill is needed based on these keywords:

- persona
- buyer persona
- customer segment
- ICP
- ideal customer profile
- jobs to be done
- JTBD
- message market fit
- customer analysis
- market segmentation
- target audience
- customer profile

## Additional Methods

### Create Message Map

```python
result = await adapter.create_message_map(
    persona_id="persona_1",
    value_proposition="Fastest content creation tool",
    proof_points=["50% faster", "Used by 1000+ teams", "99.9% uptime"],
    objections=["Too expensive", "Complex to use"]
)
```

### Prioritize Personas

```python
result = await adapter.prioritize_personas(
    personas=personas_list,
    criteria={'impact': 0.5, 'fit': 0.3, 'access': 0.2}
)
```

### Generate ICP Scorecard

```python
result = await adapter.generate_icp_scorecard(
    persona=persona_obj,
    lead_attributes=['company_size', 'industry', 'technology_stack']
)
```

### Analyze Persona Gaps

```python
result = await adapter.analyze_persona_gaps(
    personas=current_personas,
    market_coverage=['Healthcare', 'Finance', 'Retail', 'Technology']
)
```

## Output Files

When executed, the skill generates:

- `customer-personas.json`: Complete persona analysis with all data
- Located in: `{output_directory}/customer-personas.json`

## Integration with Other Skills

This skill works well with:

- **data-analyzer**: Analyze CRM and customer data before persona creation
- **xlsx**: Export persona data to spreadsheets
- **pdf**: Create persona presentation documents
- **pptx**: Build persona presentation decks

## Best Practices

1. **Provide as much input data as possible**: The more context you provide, the better the personas
2. **Include real customer evidence**: CRM data, interview transcripts, support tickets
3. **Define clear strategic goals**: Helps prioritize personas correctly
4. **Validate with real customers**: Use generated personas as hypotheses to test
5. **Iterate based on feedback**: Update personas as you learn more

## Technical Details

- **Category**: marketing
- **Version**: 1.0.0
- **Dependencies**: pandas, pydantic
- **Input Formats**: JSON, YAML, CSV, text
- **Output Formats**: JSON, Markdown, PDF
- **Adapter Class**: `MarketingSkillsAdapter`
- **Handler Method**: `_execute_persona_skill`

## Schema

### Persona Object Schema

```json
{
  "id": "string",
  "label": "string",
  "type": "B2B|B2C",
  "role_or_archetype": "string",
  "company": {
    "industry": "string",
    "size": "micro|SMB|mid|enterprise"
  },
  "geos": ["string"],
  "jtbd": ["When I..., I want..., so that..."],
  "pains": ["string"],
  "gains": ["string"],
  "triggers": ["string"],
  "decision_criteria": ["string"],
  "objections": ["string"],
  "reassurances": ["string"],
  "channels_formats": ["LinkedIn", "Email", "SEO"],
  "message_map": {
    "promise": "string",
    "proof_points": ["string"],
    "cta": "string",
    "angles": ["string"]
  },
  "offers_pricing_hooks": ["string"],
  "intent_signals": ["string"],
  "priority_scores": {
    "impact": 0-5,
    "fit": 0-5,
    "access": 0-5,
    "total": 0-15
  },
  "notes": "string"
}
```

## Contributing

To enhance this skill:

1. Add new methods to `MarketingSkillsAdapter` in `integrations/skill_adapters/marketing_skills.py`
2. Update the skill manifest in `config/skills-manifest.yaml`
3. Add new keywords to task planner in `orchestrator/task_planner.py`
4. Update this documentation

## Support

For issues or questions about this skill:
- Review the main framework documentation in `CLAUDE.md`
- Check the implementation in `integrations/skill_adapters/marketing_skills.py`
- See example usage in framework tests
