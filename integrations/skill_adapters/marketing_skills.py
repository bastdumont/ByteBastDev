"""
Marketing Skills Adapter
Adapter for marketing and customer analysis skills (customer-persona-identification)
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json


class MarketingSkillsAdapter:
    """
    Adapter for marketing skills
    Handles customer-persona-identification and related marketing capabilities
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize marketing skills adapter

        Args:
            config: Configuration including skills path
        """
        self.config = config
        self.skills_path = Path(config.get('skills_path', '/mnt/skills'))
        self.output_dir = Path(config.get('output_dir', './output'))

    async def identify_customer_personas(
        self,
        company_overview: Optional[str] = None,
        products_services: Optional[List[Dict[str, Any]]] = None,
        target_markets: Optional[List[str]] = None,
        evidence_sources: Optional[Dict[str, Any]] = None,
        constraints: Optional[Dict[str, Any]] = None,
        strategic_goals: Optional[Dict[str, Any]] = None,
        max_personas: int = 6
    ) -> Dict[str, Any]:
        """
        Identify and segment customer personas from business and market data

        Args:
            company_overview: Company context, value proposition, differentiation
            products_services: List of products/services with pricing
            target_markets: Target segments (B2B/B2C, sectors, sizes, countries)
            evidence_sources: Available data (CRM, interviews, analytics, etc.)
            constraints: Compliance, languages, channels, budget constraints
            strategic_goals: KPIs (MRR/ARR, CAC/LTV, win rate, churn, etc.)
            max_personas: Maximum number of personas to generate (1-6)

        Returns:
            Customer persona analysis with personas, gaps, and next steps
        """
        # Build context for persona generation
        context = {
            'company_overview': company_overview or 'Not provided',
            'products_services': products_services or [],
            'target_markets': target_markets or [],
            'evidence_sources': evidence_sources or {},
            'constraints': constraints or {},
            'strategic_goals': strategic_goals or {}
        }

        # Generate sample personas structure (in real implementation, this would
        # call Claude with the skill prompt to generate actual personas)
        personas = self._generate_persona_structure(context, max_personas)

        # Analyze gaps in available data
        gaps = self._identify_data_gaps(context)

        # Generate next steps recommendations
        next_steps = self._generate_next_steps(context, personas, gaps)

        result = {
            'success': True,
            'personas': personas,
            'gaps': gaps,
            'next_steps': next_steps,
            'summary': {
                'total_personas': len(personas),
                'top_priority': personas[0]['id'] if personas else None,
                'data_completeness': self._calculate_completeness(context),
                'recommended_action': next_steps[0] if next_steps else 'Review personas'
            }
        }

        # Save results to output directory
        output_path = self.output_dir / 'customer-personas.json'
        self._save_personas(result, output_path)

        return result

    def _generate_persona_structure(
        self,
        context: Dict[str, Any],
        max_personas: int
    ) -> List[Dict[str, Any]]:
        """Generate persona structure based on context"""
        personas = []

        # Determine persona type from target markets
        is_b2b = any('B2B' in str(market).upper() for market in context.get('target_markets', []))
        persona_type = 'B2B' if is_b2b else 'B2C'

        # Generate placeholder personas (real implementation would use AI)
        num_personas = min(max_personas, 3)  # Start with 3 as default

        for i in range(num_personas):
            persona = {
                'id': f'persona_{i+1}',
                'label': f'Customer Segment {i+1}',
                'type': persona_type,
                'role_or_archetype': 'To be determined from analysis',
                'company': {
                    'industry': 'Various',
                    'size': 'SMB' if is_b2b else 'N/A'
                },
                'geos': context.get('target_markets', ['Global']),
                'jtbd': [
                    'When I need to solve a problem, I want a solution, to achieve my goals'
                ],
                'pains': ['Pain points to be identified from data'],
                'gains': ['Expected benefits to be identified'],
                'triggers': ['Purchase triggers to be identified'],
                'decision_criteria': ['Decision criteria to be defined'],
                'objections': ['Objections to be identified'],
                'reassurances': ['Reassurances to be developed'],
                'channels_formats': ['LinkedIn', 'Email', 'SEO'],
                'message_map': {
                    'promise': 'Core value proposition',
                    'proof_points': [
                        'Proof point 1',
                        'Proof point 2',
                        'Proof point 3'
                    ],
                    'cta': 'Primary call to action',
                    'angles': ['Angle 1', 'Angle 2']
                },
                'offers_pricing_hooks': ['Offer structure to be defined'],
                'intent_signals': ['Intent signals to be identified'],
                'priority_scores': {
                    'impact': 3,
                    'fit': 3,
                    'access': 3,
                    'total': 9
                },
                'notes': 'Requires more data for detailed analysis'
            }
            personas.append(persona)

        return personas

    def _identify_data_gaps(self, context: Dict[str, Any]) -> List[str]:
        """Identify missing data that would improve persona definition"""
        gaps = []

        if not context.get('company_overview'):
            gaps.append('Company overview and value proposition needed')

        if not context.get('products_services'):
            gaps.append('Product/service details and pricing information needed')

        if not context.get('evidence_sources') or not context['evidence_sources']:
            gaps.append('Customer data sources (CRM, interviews, analytics) needed')

        if not context.get('target_markets'):
            gaps.append('Target market segments definition needed')

        if not context.get('strategic_goals'):
            gaps.append('Strategic goals and KPIs needed for prioritization')

        return gaps

    def _generate_next_steps(
        self,
        context: Dict[str, Any],
        personas: List[Dict[str, Any]],
        gaps: List[str]
    ) -> List[str]:
        """Generate recommended next steps"""
        next_steps = []

        if gaps:
            next_steps.append(f'Gather missing data: {len(gaps)} critical gaps identified')

        next_steps.append('Conduct customer interviews to validate persona hypotheses')
        next_steps.append('Analyze existing customer data (CRM, support tickets, analytics)')
        next_steps.append('Create message maps and content for top 2 priority personas')
        next_steps.append('Design A/B tests for channel and messaging hypotheses')
        next_steps.append('Develop ICP (Ideal Customer Profile) scoring model')

        return next_steps

    def _calculate_completeness(self, context: Dict[str, Any]) -> float:
        """Calculate data completeness percentage"""
        fields = [
            'company_overview',
            'products_services',
            'target_markets',
            'evidence_sources',
            'constraints',
            'strategic_goals'
        ]

        filled_fields = sum(1 for field in fields if context.get(field))
        return round((filled_fields / len(fields)) * 100, 1)

    def _save_personas(self, result: Dict[str, Any], output_path: Path) -> None:
        """Save persona analysis to file"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    async def create_message_map(
        self,
        persona_id: str,
        value_proposition: str,
        proof_points: List[str],
        objections: List[str]
    ) -> Dict[str, Any]:
        """
        Create detailed message map for a specific persona

        Args:
            persona_id: Target persona identifier
            value_proposition: Core value proposition
            proof_points: Evidence supporting the value proposition
            objections: Common objections to address

        Returns:
            Message map with promise, proof, objection handling, and CTAs
        """
        return {
            'success': True,
            'persona_id': persona_id,
            'message_map': {
                'promise': value_proposition,
                'proof_points': proof_points,
                'objection_handling': [
                    {'objection': obj, 'response': f'Response to: {obj}'}
                    for obj in objections
                ],
                'cta_primary': 'Book a demo',
                'cta_secondary': 'Download case study',
                'channels': ['LinkedIn', 'Email', 'Website']
            }
        }

    async def prioritize_personas(
        self,
        personas: List[Dict[str, Any]],
        criteria: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Prioritize personas based on impact, fit, and access scores

        Args:
            personas: List of persona objects
            criteria: Weighting criteria for prioritization
                     (e.g., {'impact': 0.5, 'fit': 0.3, 'access': 0.2})

        Returns:
            Prioritized personas with scores and recommendations
        """
        # Default equal weighting
        criteria = criteria or {'impact': 0.33, 'fit': 0.33, 'access': 0.34}

        # Calculate weighted scores
        for persona in personas:
            scores = persona.get('priority_scores', {})
            weighted_score = (
                scores.get('impact', 0) * criteria['impact'] +
                scores.get('fit', 0) * criteria['fit'] +
                scores.get('access', 0) * criteria['access']
            )
            persona['weighted_priority'] = round(weighted_score, 2)

        # Sort by weighted priority
        prioritized = sorted(
            personas,
            key=lambda p: p.get('weighted_priority', 0),
            reverse=True
        )

        return {
            'success': True,
            'prioritized_personas': prioritized,
            'top_priority': prioritized[0] if prioritized else None,
            'criteria_used': criteria
        }

    async def generate_icp_scorecard(
        self,
        persona: Dict[str, Any],
        lead_attributes: List[str]
    ) -> Dict[str, Any]:
        """
        Generate ICP (Ideal Customer Profile) scorecard for lead scoring

        Args:
            persona: Target persona definition
            lead_attributes: Attributes to score (company size, industry, etc.)

        Returns:
            Scorecard with scoring rules and thresholds
        """
        scorecard = {
            'persona_id': persona.get('id'),
            'persona_label': persona.get('label'),
            'scoring_attributes': []
        }

        # Generate scoring rules for each attribute
        for attr in lead_attributes:
            scorecard['scoring_attributes'].append({
                'attribute': attr,
                'weight': 10,
                'scoring_rules': [
                    {'condition': f'{attr} matches ideal', 'points': 10},
                    {'condition': f'{attr} partially matches', 'points': 5},
                    {'condition': f'{attr} does not match', 'points': 0}
                ]
            })

        scorecard['thresholds'] = {
            'hot_lead': 70,
            'warm_lead': 40,
            'cold_lead': 0
        }

        return {
            'success': True,
            'scorecard': scorecard
        }

    async def analyze_persona_gaps(
        self,
        personas: List[Dict[str, Any]],
        market_coverage: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze gaps in persona coverage vs. total addressable market

        Args:
            personas: Current persona definitions
            market_coverage: Market segments that should be covered

        Returns:
            Gap analysis with uncovered segments and recommendations
        """
        covered_segments = set()
        for persona in personas:
            if persona.get('company', {}).get('industry'):
                covered_segments.add(persona['company']['industry'])

        uncovered = set(market_coverage) - covered_segments

        return {
            'success': True,
            'covered_segments': list(covered_segments),
            'uncovered_segments': list(uncovered),
            'coverage_percentage': round(
                (len(covered_segments) / len(market_coverage) * 100) if market_coverage else 0,
                1
            ),
            'recommendations': [
                f'Develop persona for {segment}' for segment in uncovered
            ]
        }
