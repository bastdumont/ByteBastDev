import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight, Sparkles } from 'lucide-react'

export function Hero() {
  return (
    <section className="container flex flex-col items-center gap-8 pt-20 pb-16 md:pt-28 md:pb-24">
      <div className="flex max-w-[980px] flex-col items-center gap-4 text-center">
        <div className="inline-flex items-center rounded-lg bg-muted px-3 py-1 text-sm font-medium">
          <Sparkles className="mr-2 h-4 w-4" />
          <span>Introducing our SaaS Platform</span>
        </div>

        <h1 className="text-4xl font-bold leading-tight tracking-tighter md:text-6xl lg:text-7xl">
          Build your business
          <br className="hidden sm:inline" />
          {' '}with our platform
        </h1>

        <p className="max-w-[750px] text-lg text-muted-foreground sm:text-xl">
          The complete solution for modern businesses. Ship faster with our
          production-ready SaaS starter kit.
        </p>

        <div className="flex gap-4">
          <Button size="lg" asChild>
            <Link href="/register">
              Get Started
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
          <Button size="lg" variant="outline" asChild>
            <Link href="#pricing">View Pricing</Link>
          </Button>
        </div>
      </div>

      <div className="relative mt-8 w-full max-w-[1200px] overflow-hidden rounded-xl border bg-background shadow-2xl">
        <div className="aspect-video bg-gradient-to-br from-primary/10 via-primary/5 to-background">
          {/* Add your demo image or video here */}
          <div className="flex h-full items-center justify-center text-muted-foreground">
            Dashboard Preview
          </div>
        </div>
      </div>
    </section>
  )
}
