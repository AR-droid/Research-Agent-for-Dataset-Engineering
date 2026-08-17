export default function ReviewsPage() {
  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Human Reviews</h1>
        <p className="text-muted-foreground mt-2">Review flags, ambiguous data points, and agent confidence scores.</p>
      </div>

      <div className="border rounded-md">
        <div className="p-12 text-center text-muted-foreground flex flex-col items-center justify-center">
          <p>No pending reviews.</p>
        </div>
      </div>
    </div>
  );
}
