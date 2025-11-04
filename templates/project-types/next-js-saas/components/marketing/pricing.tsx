import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Check } from 'lucide-react'
import Link from 'next/link'

const pricingPlans = [
  {
    name: 'Starter',
    description: 'Perfect for individuals and small teams',
    price: '$19',
    priceId: process.env.STRIPE_PRICE_ID_STARTER,
    features: [
      '10 projects',
      '5GB storage',
      'Basic analytics',
      'Email support',
      'Community access',
    ],
  },
  {
    name: 'Pro',
    description: 'For growing businesses and teams',
    price: '$49',
    priceId: process.env.STRIPE_PRICE_ID_PRO,
    features: [
      'Unlimited projects',
      '50GB storage',
      'Advanced analytics',
      'Priority support',
      'Custom integrations',
      'Team collaboration',
    ],
    popular: true,
  },
  {
    name: 'Enterprise',
    description: 'For large organizations',
    price: '$199',
    priceId: process.env.STRIPE_PRICE_ID_ENTERPRISE,
    features: [
      'Unlimited everything',
      '500GB storage',
      'Custom analytics',
      '24/7 phone support',
      'Dedicated account manager',
      'Custom contracts',
      'SLA guarantee',
    ],
  },
]

export function Pricing() {
  return (
    <section id="pricing" className="container py-16 md:py-24">
      <div className="mx-auto flex max-w-[980px] flex-col items-center gap-4 text-center">
        <h2 className="text-3xl font-bold leading-tight tracking-tighter md:text-5xl">
          Simple, transparent pricing
        </h2>
        <p className="max-w-[750px] text-lg text-muted-foreground">
          Choose the plan that works best for you. All plans include a 14-day free trial.
        </p>
      </div>

      <div className="mx-auto mt-12 grid max-w-5xl gap-8 md:grid-cols-3">
        {pricingPlans.map((plan) => (
          <Card
            key={plan.name}
            className={plan.popular ? 'border-primary shadow-lg' : ''}
          >
            <CardHeader>
              {plan.popular && (
                <div className="mb-2 inline-block w-fit rounded-full bg-primary px-3 py-1 text-xs font-semibold text-primary-foreground">
                  Most Popular
                </div>
              )}
              <CardTitle>{plan.name}</CardTitle>
              <CardDescription>{plan.description}</CardDescription>
              <div className="mt-4">
                <span className="text-4xl font-bold">{plan.price}</span>
                <span className="text-muted-foreground">/month</span>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center">
                    <Check className="mr-2 h-4 w-4 text-primary" />
                    <span className="text-sm">{feature}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
            <CardFooter>
              <Button
                className="w-full"
                variant={plan.popular ? 'default' : 'outline'}
                asChild
              >
                <Link href="/register">Get Started</Link>
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </section>
  )
}
