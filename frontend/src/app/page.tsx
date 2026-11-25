export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-6 py-16">
      <p className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-500">
        Kenyan CBE Assessment Management
      </p>
      <h1 className="mt-4 max-w-3xl text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl">
        Assessment and learner portfolios, built around CBE.
      </h1>
      <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-600">
        A focused platform for competency assessment, Senior School pathway insights,
        and secure parent access to learner reports.
      </p>
      <div className="mt-10 grid gap-4 sm:grid-cols-3">
        {[
          ["CBE assessment", "Structured learning areas, strands, sub-strands and rubrics."],
          ["Pathway insights", "Evidence-led readiness analysis from Grades 7–9."],
          ["Learner portfolios", "Secure report access with Paystack payment workflows."],
        ].map(([title, description]) => (
          <section key={title} className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="font-semibold text-slate-900">{title}</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">{description}</p>
          </section>
        ))}
      </div>
      <p className="mt-12 text-xs text-slate-500">MVP scaffold · Development environment</p>
    </main>
  );
}
