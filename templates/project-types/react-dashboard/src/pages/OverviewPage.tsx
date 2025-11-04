import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { RevenueChart } from '@/components/charts/RevenueChart'
import { UsersChart } from '@/components/charts/UsersChart'
import { RecentActivity } from '@/components/RecentActivity'
import { StatsCards } from '@/components/StatsCards'
import { useQuery } from '@tanstack/react-query'
import { getOverviewStats } from '@/api/dashboard'

export function OverviewPage() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['overview-stats'],
    queryFn: getOverviewStats,
  })

  if (isLoading) {
    return <div className="p-8">Loading...</div>
  }

  return (
    <div className="flex flex-col gap-6 p-8">
      <div>
        <h1 className="text-3xl font-bold">Dashboard Overview</h1>
        <p className="text-muted-foreground">
          Welcome back! Here's what's happening with your business today.
        </p>
      </div>

      <StatsCards stats={stats?.stats} />

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Revenue</CardTitle>
          </CardHeader>
          <CardContent>
            <RevenueChart data={stats?.revenueData} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>User Growth</CardTitle>
          </CardHeader>
          <CardContent>
            <UsersChart data={stats?.usersData} />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <RecentActivity activities={stats?.recentActivity} />
        </CardContent>
      </Card>
    </div>
  )
}
