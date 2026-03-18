import { useState, useMemo } from "react";

const IMPUGNED_DAYS = [
  { date: "2023-08-31", index: "BANKNIFTY", strategy: "Intraday", profit: 191.59 },
  { date: "2023-09-13", index: "BANKNIFTY", strategy: "Intraday", profit: 212.18 },
  { date: "2023-09-20", index: "BANKNIFTY", strategy: "Intraday", profit: 233.13 },
  { date: "2023-09-28", index: "BANKNIFTY", strategy: "Intraday", profit: 241.69 },
  { date: "2023-10-04", index: "BANKNIFTY", strategy: "Ext. Close", profit: 163.67 },
  { date: "2023-10-18", index: "BANKNIFTY", strategy: "Intraday", profit: 317.33 },
  { date: "2023-10-26", index: "BANKNIFTY", strategy: "Intraday", profit: 259.12 },
  { date: "2023-12-06", index: "BANKNIFTY", strategy: "Intraday", profit: 150.90 },
  { date: "2024-01-03", index: "BANKNIFTY", strategy: "Intraday", profit: 164.65 },
  { date: "2024-01-17", index: "BANKNIFTY", strategy: "Intraday", profit: 734.93 },
  { date: "2024-03-06", index: "BANKNIFTY", strategy: "Intraday", profit: 197.05 },
  { date: "2024-04-16", index: "BANKNIFTY", strategy: "Intraday", profit: 170.27 },
  { date: "2024-05-08", index: "BANKNIFTY", strategy: "Intraday", profit: 171.01 },
  { date: "2024-05-15", index: "BANKNIFTY", strategy: "Intraday", profit: 160.72 },
  { date: "2024-05-29", index: "BANKNIFTY", strategy: "Intraday", profit: 258.55 },
  { date: "2024-06-19", index: "BANKNIFTY", strategy: "Ext. Close", profit: 322.45 },
  { date: "2024-07-03", index: "BANKNIFTY", strategy: "Intraday", profit: 299.03 },
  { date: "2024-07-10", index: "BANKNIFTY", strategy: "Ext. Close", profit: 225.35 },
  { date: "2025-05-08", index: "NIFTY", strategy: "Ext. Close", profit: 3.07 },
  { date: "2025-05-15", index: "NIFTY", strategy: "Ext. Close", profit: 167.53 },
  { date: "2025-05-22", index: "NIFTY", strategy: "Ext. Close", profit: 199.36 },
];

const ENTITIES = [
  { id: "E1", name: "Jane Street Asia Trading Ltd", pan: "AAECJ7368M", region: "Hong Kong", type: "FPI", indexOpt: 7650.34, total: 6929.56 },
  { id: "E2", name: "JSI2 Investments Pvt Ltd", pan: "AAGCJ5786R", region: "India", type: "Domestic", indexOpt: -168.67, total: -168.67 },
  { id: "E3", name: "JSI Investments Pvt Ltd", pan: "AAFCJ0285L", region: "India", type: "Domestic", indexOpt: 4392.03, total: 4104.61 },
  { id: "E4", name: "Jane Street Singapore Pte Ltd", pan: "AAGCJ1682G", region: "Singapore", type: "FPI", indexOpt: 31415.63, total: 25636.62 },
];

const TIMELINE = [
  { date: "2023-01", label: "Exam period starts", type: "regulatory" },
  { date: "2023-08", label: "First impugned day", type: "trading" },
  { date: "2024-01", label: "Peak profit day (₹735 Cr)", type: "trading" },
  { date: "2024-04", label: "US lawsuit filed vs Millennium", type: "legal" },
  { date: "2024-07", label: "NSE asked to examine", type: "regulatory" },
  { date: "2024-12", label: "US case settled", type: "legal" },
  { date: "2025-02", label: "Caution letter issued", type: "regulatory" },
  { date: "2025-03", label: "Exam period ends", type: "regulatory" },
  { date: "2025-05", label: "Post-caution violations", type: "trading" },
  { date: "2025-07", label: "SEBI interim order", type: "regulatory" },
  { date: "2026-02", label: "SAT hearings ongoing", type: "legal" },
];

const JAN17 = [
  { time: "09:15", phase: "open", idx: 46072, label: "Market opens down (HDFC earnings)" },
  { time: "09:16", phase: "patch1", idx: 46814, label: "Patch I: JS aggressive buying begins" },
  { time: "09:17", phase: "patch1", idx: 46879, label: "" },
  { time: "09:18", phase: "patch1", idx: 47015, label: "" },
  { time: "09:19", phase: "patch1", idx: 47060, label: "" },
  { time: "09:20", phase: "patch1", idx: 47107, label: "" },
  { time: "09:21", phase: "patch1", idx: 47144, label: "" },
  { time: "09:22", phase: "patch1", idx: 47177, label: "Patch I ends: +1105 pts in 7 min" },
  { time: "10:00", phase: "neutral", idx: 47100, label: "Neutral / options positioning" },
  { time: "11:00", phase: "neutral", idx: 47050, label: "" },
  { time: "11:45", phase: "transition", idx: 46950, label: "Patch II: reversal begins" },
  { time: "12:30", phase: "patch2", idx: 46700, label: "Aggressive selling" },
  { time: "13:30", phase: "patch2", idx: 46400, label: "" },
  { time: "14:30", phase: "patch2", idx: 46200, label: "" },
  { time: "15:29", phase: "patch2", idx: 46000, label: "Near close: options profit realized" },
];

const Pill = ({ children, active, onClick }) => (
  <button
    onClick={onClick}
    style={{
      padding: "6px 16px",
      borderRadius: 20,
      border: active ? "1.5px solid #e8590c" : "1.5px solid #3a3a3a",
      background: active ? "#e8590c" : "transparent",
      color: active ? "#fff" : "#b0b0b0",
      fontSize: 13,
      fontFamily: "'JetBrains Mono', monospace",
      cursor: "pointer",
      transition: "all 0.2s",
    }}
  >
    {children}
  </button>
);

const Card = ({ children, style }) => (
  <div style={{
    background: "#1a1a1a",
    border: "1px solid #2a2a2a",
    borderRadius: 8,
    padding: 20,
    ...style,
  }}>{children}</div>
);

const Stat = ({ label, value, sub }) => (
  <div style={{ textAlign: "center" }}>
    <div style={{ fontSize: 11, color: "#777", fontFamily: "'JetBrains Mono', monospace", textTransform: "uppercase", letterSpacing: 1.5 }}>{label}</div>
    <div style={{ fontSize: 28, fontWeight: 700, color: "#f0f0f0", fontFamily: "'JetBrains Mono', monospace", marginTop: 4 }}>{value}</div>
    {sub && <div style={{ fontSize: 11, color: "#e8590c", marginTop: 2 }}>{sub}</div>}
  </div>
);

export default function Dashboard() {
  const [tab, setTab] = useState("overview");
  const [stratFilter, setStratFilter] = useState("all");

  const filtered = useMemo(() => {
    if (stratFilter === "all") return IMPUGNED_DAYS;
    if (stratFilter === "intraday") return IMPUGNED_DAYS.filter(d => d.strategy === "Intraday");
    return IMPUGNED_DAYS.filter(d => d.strategy === "Ext. Close");
  }, [stratFilter]);

  const totalProfit = filtered.reduce((s, d) => s + d.profit, 0);
  const maxDay = filtered.reduce((m, d) => d.profit > m.profit ? d : m, filtered[0]);
  const maxBar = Math.max(...IMPUGNED_DAYS.map(d => d.profit));

  return (
    <div style={{
      background: "#111",
      color: "#e0e0e0",
      minHeight: "100vh",
      fontFamily: "'Inter', sans-serif",
      padding: "24px 20px",
    }}>
      <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />

      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        <div style={{ marginBottom: 32 }}>
          <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: "#e8590c", letterSpacing: 2, textTransform: "uppercase", marginBottom: 4 }}>
            Forensic Reconstruction
          </div>
          <h1 style={{ fontSize: 26, fontWeight: 700, color: "#f5f5f5", margin: 0, lineHeight: 1.2 }}>
            Jane Street India — Case Data Overview
          </h1>
          <p style={{ fontSize: 13, color: "#666", margin: "8px 0 0", fontFamily: "'JetBrains Mono', monospace" }}>
            SEBI Interim Order WTM/AN/MRD/MRD-SEC-3/31516/2025-26 · 21 impugned days · 4 entities
          </p>
        </div>

        <div style={{ display: "flex", gap: 8, marginBottom: 24, flexWrap: "wrap" }}>
          {["overview", "days", "jan17", "entities", "pipeline"].map(t => (
            <Pill key={t} active={tab === t} onClick={() => setTab(t)}>
              {t === "overview" ? "Overview" : t === "days" ? "Impugned Days" : t === "jan17" ? "Jan 17 Deep Dive" : t === "entities" ? "Entities" : "Research Pipeline"}
            </Pill>
          ))}
        </div>

        {tab === "overview" && (
          <div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 24 }}>
              <Card><Stat label="Total Alleged Gains" value="₹4,844 Cr" sub="~$576M USD" /></Card>
              <Card><Stat label="Impugned Days" value="21" sub="18 exam + 3 post" /></Card>
              <Card><Stat label="Entities" value="4" sub="2 FPI + 2 domestic" /></Card>
              <Card><Stat label="Peak Day Profit" value="₹735 Cr" sub="Jan 17, 2024" /></Card>
            </div>

            <Card style={{ marginBottom: 24 }}>
              <div style={{ fontSize: 12, color: "#888", fontFamily: "'JetBrains Mono', monospace", marginBottom: 16, textTransform: "uppercase", letterSpacing: 1.2 }}>
                Case Timeline
              </div>
              <div style={{ position: "relative", paddingLeft: 20 }}>
                {TIMELINE.map((ev, i) => (
                  <div key={i} style={{ display: "flex", alignItems: "flex-start", marginBottom: 12, position: "relative" }}>
                    <div style={{
                      position: "absolute", left: -20, top: 4,
                      width: 10, height: 10, borderRadius: "50%",
                      background: ev.type === "regulatory" ? "#e8590c" : ev.type === "legal" ? "#4dabf7" : "#51cf66",
                      border: "2px solid #111",
                    }} />
                    {i < TIMELINE.length - 1 && (
                      <div style={{ position: "absolute", left: -16, top: 14, width: 2, height: 22, background: "#2a2a2a" }} />
                    )}
                    <div style={{ marginLeft: 8 }}>
                      <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: "#666", marginRight: 12 }}>{ev.date}</span>
                      <span style={{ fontSize: 13, color: "#ccc" }}>{ev.label}</span>
                    </div>
                  </div>
                ))}
              </div>
              <div style={{ display: "flex", gap: 16, marginTop: 12, borderTop: "1px solid #2a2a2a", paddingTop: 10 }}>
                {[["#e8590c", "Regulatory"], ["#4dabf7", "Legal"], ["#51cf66", "Trading"]].map(([c, l]) => (
                  <div key={l} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 11, color: "#888" }}>
                    <div style={{ width: 8, height: 8, borderRadius: "50%", background: c }} />{l}
                  </div>
                ))}
              </div>
            </Card>

            <Card>
              <div style={{ fontSize: 12, color: "#888", fontFamily: "'JetBrains Mono', monospace", marginBottom: 12, textTransform: "uppercase", letterSpacing: 1.2 }}>
                Strategy Breakdown
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
                <div style={{ padding: 16, background: "#222", borderRadius: 6, borderLeft: "3px solid #e8590c" }}>
                  <div style={{ fontSize: 14, fontWeight: 600, color: "#f0f0f0" }}>Intra-day Index Manipulation</div>
                  <div style={{ fontSize: 12, color: "#999", marginTop: 6, lineHeight: 1.6 }}>
                    15 of 18 exam-period days. Two-phase: Patch I aggressive buying of constituents → Patch II reversal selling. Options positioned between phases. Accept equity/futures loss to profit massively on index options.
                  </div>
                  <div style={{ marginTop: 8, fontFamily: "'JetBrains Mono', monospace", fontSize: 13, color: "#e8590c" }}>
                    ₹199.7 Cr total loss on equities → offset by options gains
                  </div>
                </div>
                <div style={{ padding: 16, background: "#222", borderRadius: 6, borderLeft: "3px solid #4dabf7" }}>
                  <div style={{ fontSize: 14, fontWeight: 600, color: "#f0f0f0" }}>Extended Marking the Close</div>
                  <div style={{ fontSize: 12, color: "#999", marginTop: 6, lineHeight: 1.6 }}>
                    3 exam-period days + 3 post-caution days (May 2025, NIFTY). Concentrated trading in final 30 min to skew closing index level. Options pre-positioned to profit from engineered settlement price.
                  </div>
                  <div style={{ marginTop: 8, fontFamily: "'JetBrains Mono', monospace", fontSize: 13, color: "#4dabf7" }}>
                    6 total days including post-caution NIFTY violations
                  </div>
                </div>
              </div>
            </Card>
          </div>
        )}

        {tab === "days" && (
          <div>
            <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
              {[["all", "All (21)"], ["intraday", "Intraday (15)"], ["close", "Ext. Close (6)"]].map(([k, l]) => (
                <Pill key={k} active={stratFilter === k} onClick={() => setStratFilter(k)}>{l}</Pill>
              ))}
            </div>

            <Card style={{ marginBottom: 20 }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 12 }}>
                <div style={{ fontSize: 12, color: "#888", fontFamily: "'JetBrains Mono', monospace", textTransform: "uppercase", letterSpacing: 1.2 }}>
                  Profit by Day (₹ Crore)
                </div>
                <div style={{ fontSize: 12, color: "#e8590c", fontFamily: "'JetBrains Mono', monospace" }}>
                  Total: ₹{totalProfit.toFixed(1)} Cr
                </div>
              </div>
              <div style={{ display: "flex", alignItems: "flex-end", gap: 3, height: 180, paddingTop: 10 }}>
                {filtered.map((d, i) => {
                  const h = (d.profit / maxBar) * 160;
                  const isMax = d === maxDay;
                  return (
                    <div key={i} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", position: "relative" }}>
                      {isMax && (
                        <div style={{ fontSize: 9, color: "#e8590c", fontFamily: "'JetBrains Mono', monospace", marginBottom: 2, whiteSpace: "nowrap" }}>
                          ₹{d.profit.toFixed(0)}
                        </div>
                      )}
                      <div
                        title={`${d.date}: ₹${d.profit} Cr (${d.strategy})`}
                        style={{
                          width: "100%",
                          maxWidth: 32,
                          height: h,
                          background: d.strategy === "Intraday"
                            ? `linear-gradient(180deg, #e8590c, #c2410c)`
                            : `linear-gradient(180deg, #4dabf7, #1c7ed6)`,
                          borderRadius: "3px 3px 0 0",
                          opacity: isMax ? 1 : 0.7,
                          cursor: "pointer",
                          transition: "opacity 0.2s",
                        }}
                        onMouseEnter={e => e.target.style.opacity = 1}
                        onMouseLeave={e => { if (!isMax) e.target.style.opacity = 0.7; }}
                      />
                      <div style={{
                        fontSize: 8, color: "#555", marginTop: 4,
                        fontFamily: "'JetBrains Mono', monospace",
                        transform: "rotate(-45deg)", transformOrigin: "left",
                        whiteSpace: "nowrap",
                      }}>
                        {d.date.slice(2, 7)}
                      </div>
                    </div>
                  );
                })}
              </div>
            </Card>

            <Card>
              <div style={{ fontSize: 12, color: "#888", fontFamily: "'JetBrains Mono', monospace", marginBottom: 12, textTransform: "uppercase", letterSpacing: 1.2 }}>
                Day Detail Table
              </div>
              <div style={{ overflowX: "auto" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, fontFamily: "'JetBrains Mono', monospace" }}>
                  <thead>
                    <tr style={{ borderBottom: "1px solid #333" }}>
                      {["#", "Date", "Index", "Strategy", "Profit (₹ Cr)", "Exam Period"].map(h => (
                        <th key={h} style={{ padding: "8px 10px", textAlign: "left", color: "#666", fontWeight: 500, fontSize: 10, textTransform: "uppercase" }}>{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map((d, i) => {
                      const inExam = d.date < "2025-04";
                      return (
                        <tr key={i} style={{ borderBottom: "1px solid #1f1f1f" }}>
                          <td style={{ padding: "7px 10px", color: "#555" }}>{i + 1}</td>
                          <td style={{ padding: "7px 10px", color: "#ddd" }}>{d.date}</td>
                          <td style={{ padding: "7px 10px", color: d.index === "NIFTY" ? "#ffd43b" : "#e8590c" }}>{d.index}</td>
                          <td style={{ padding: "7px 10px" }}>
                            <span style={{
                              padding: "2px 8px", borderRadius: 10, fontSize: 10,
                              background: d.strategy === "Intraday" ? "#e8590c22" : "#4dabf722",
                              color: d.strategy === "Intraday" ? "#e8590c" : "#4dabf7",
                            }}>{d.strategy}</span>
                          </td>
                          <td style={{ padding: "7px 10px", color: "#51cf66", fontWeight: 600 }}>₹{d.profit.toFixed(2)}</td>
                          <td style={{ padding: "7px 10px", color: inExam ? "#51cf66" : "#ffd43b" }}>{inExam ? "Yes" : "Post-caution"}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </Card>
          </div>
        )}

        {tab === "jan17" && (
          <div>
            <Card style={{ marginBottom: 20 }}>
              <div style={{ fontSize: 12, color: "#888", fontFamily: "'JetBrains Mono', monospace", marginBottom: 4, textTransform: "uppercase", letterSpacing: 1.2 }}>
                January 17, 2024 — BANKNIFTY Intraday Manipulation
              </div>
              <div style={{ fontSize: 13, color: "#aaa", marginBottom: 20 }}>
                Peak profit day: ₹734.93 Cr. HDFC Bank earnings miss → JS buys all 12 constituents for 7 min → establishes options → reverses and sells all afternoon.
              </div>

              <svg viewBox="0 0 800 300" style={{ width: "100%", height: "auto" }}>
                <defs>
                  <linearGradient id="p1" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#e8590c" stopOpacity="0.3" />
                    <stop offset="100%" stopColor="#e8590c" stopOpacity="0.02" />
                  </linearGradient>
                  <linearGradient id="p2" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#4dabf7" stopOpacity="0.3" />
                    <stop offset="100%" stopColor="#4dabf7" stopOpacity="0.02" />
                  </linearGradient>
                </defs>

                {/* Grid */}
                {[0, 1, 2, 3, 4].map(i => (
                  <g key={i}>
                    <line x1={60} y1={40 + i * 55} x2={780} y2={40 + i * 55} stroke="#222" strokeWidth={1} />
                    <text x={55} y={44 + i * 55} fill="#555" fontSize={9} textAnchor="end" fontFamily="JetBrains Mono">
                      {(47200 - i * 300).toLocaleString()}
                    </text>
                  </g>
                ))}

                {/* Patch zones */}
                <rect x={75} y={30} width={75} height={240} fill="url(#p1)" rx={4} />
                <rect x={370} y={30} width={390} height={240} fill="url(#p2)" rx={4} />

                <text x={112} y={22} fill="#e8590c" fontSize={10} textAnchor="middle" fontFamily="JetBrains Mono" fontWeight={600}>PATCH I</text>
                <text x={565} y={22} fill="#4dabf7" fontSize={10} textAnchor="middle" fontFamily="JetBrains Mono" fontWeight={600}>PATCH II</text>

                {/* Price line */}
                {(() => {
                  const pts = JAN17.map((d, i) => {
                    const x = 75 + (i / (JAN17.length - 1)) * 700;
                    const y = 40 + ((47200 - d.idx) / 1200) * 220;
                    return `${x},${y}`;
                  });
                  return (
                    <polyline
                      points={pts.join(" ")}
                      fill="none"
                      stroke="#f0f0f0"
                      strokeWidth={2}
                      strokeLinejoin="round"
                    />
                  );
                })()}

                {/* Data points */}
                {JAN17.map((d, i) => {
                  const x = 75 + (i / (JAN17.length - 1)) * 700;
                  const y = 40 + ((47200 - d.idx) / 1200) * 220;
                  const color = d.phase === "patch1" ? "#e8590c" : d.phase === "patch2" ? "#4dabf7" : "#666";
                  return (
                    <g key={i}>
                      <circle cx={x} cy={y} r={4} fill={color} stroke="#111" strokeWidth={2} />
                      <text x={x} y={280} fill="#555" fontSize={8} textAnchor="middle" fontFamily="JetBrains Mono">{d.time}</text>
                    </g>
                  );
                })}

                {/* Annotations */}
                <text x={75} y={295} fill="#e8590c" fontSize={8} fontFamily="JetBrains Mono">Open: 46,072</text>
                <text x={148} y={60} fill="#51cf66" fontSize={8} fontFamily="JetBrains Mono">Peak: 47,177</text>
                <text x={680} y={240} fill="#4dabf7" fontSize={8} fontFamily="JetBrains Mono">Close: ~46,000</text>
              </svg>
            </Card>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 20 }}>
              <Card>
                <div style={{ fontSize: 11, color: "#e8590c", fontFamily: "'JetBrains Mono', monospace", textTransform: "uppercase", letterSpacing: 1.2, marginBottom: 8 }}>
                  Patch I (09:15 – 09:22)
                </div>
                <div style={{ fontSize: 12, color: "#bbb", lineHeight: 1.7 }}>
                  <div>→ Bought all 12 BANKNIFTY constituent stocks</div>
                  <div>→ ₹4,370 Cr total position (cash + futures)</div>
                  <div>→ +272 index pts from JS vs -249 pts rest of market</div>
                  <div>→ Single largest net buyer by far</div>
                  <div>→ Simultaneously shorted ATM calls + bought ATM puts</div>
                </div>
              </Card>
              <Card>
                <div style={{ fontSize: 11, color: "#4dabf7", fontFamily: "'JetBrains Mono', monospace", textTransform: "uppercase", letterSpacing: 1.2, marginBottom: 8 }}>
                  Patch II (11:45 – 15:30)
                </div>
                <div style={{ fontSize: 12, color: "#bbb", lineHeight: 1.7 }}>
                  <div>→ Reversed all positions — became largest seller</div>
                  <div>→ ₹1,859 Cr sold in cash segment</div>
                  <div>→ ₹3,513 Cr sold via index futures</div>
                  <div>→ Index drops → calls expire worthless, puts profit</div>
                  <div>→ ₹61.6 Cr equity loss → ₹735 Cr net options profit</div>
                </div>
              </Card>
            </div>

            <Card>
              <div style={{ fontSize: 11, color: "#888", fontFamily: "'JetBrains Mono', monospace", textTransform: "uppercase", letterSpacing: 1.2, marginBottom: 12 }}>
                Options Premium Movement (ATM 47000 Strike)
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16 }}>
                {[
                  { label: "09:15 (Open)", call: "~350", put: "~145" },
                  { label: "09:22 (Post Patch I)", call: "~85", put: "~283" },
                  { label: "15:29 (Pre-Close)", call: "~65", put: "~312" },
                ].map((d, i) => (
                  <div key={i} style={{ padding: 12, background: "#222", borderRadius: 6, textAlign: "center" }}>
                    <div style={{ fontSize: 10, color: "#666", marginBottom: 6 }}>{d.label}</div>
                    <div style={{ fontSize: 13 }}>
                      <span style={{ color: "#ff6b6b" }}>CE: ₹{d.call}</span>
                      {" / "}
                      <span style={{ color: "#51cf66" }}>PE: ₹{d.put}</span>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}

        {tab === "entities" && (
          <div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 20 }}>
              {ENTITIES.map(e => (
                <Card key={e.id} style={{ borderLeft: `3px solid ${e.total > 0 ? "#51cf66" : "#ff6b6b"}` }}>
                  <div style={{ fontSize: 14, fontWeight: 600, color: "#f0f0f0", marginBottom: 4 }}>{e.name}</div>
                  <div style={{ fontSize: 11, color: "#666", fontFamily: "'JetBrains Mono', monospace", marginBottom: 10 }}>
                    PAN: {e.pan} · {e.region} · {e.type}
                  </div>
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <div>
                      <div style={{ fontSize: 10, color: "#888" }}>Index Options</div>
                      <div style={{ fontSize: 16, fontWeight: 700, fontFamily: "'JetBrains Mono', monospace", color: e.indexOpt > 0 ? "#51cf66" : "#ff6b6b" }}>
                        ₹{Math.abs(e.indexOpt).toLocaleString()} Cr
                      </div>
                    </div>
                    <div style={{ textAlign: "right" }}>
                      <div style={{ fontSize: 10, color: "#888" }}>Net Total</div>
                      <div style={{ fontSize: 16, fontWeight: 700, fontFamily: "'JetBrains Mono', monospace", color: e.total > 0 ? "#51cf66" : "#ff6b6b" }}>
                        ₹{Math.abs(e.total).toLocaleString()} Cr
                      </div>
                    </div>
                  </div>
                  {e.id === "E4" && (
                    <div style={{ marginTop: 8, padding: "6px 10px", background: "#e8590c22", borderRadius: 4, fontSize: 10, color: "#e8590c" }}>
                      Dominant entity: 70% of group index-options profit
                    </div>
                  )}
                </Card>
              ))}
            </div>

            <Card>
              <div style={{ fontSize: 11, color: "#888", fontFamily: "'JetBrains Mono', monospace", textTransform: "uppercase", letterSpacing: 1.2, marginBottom: 16 }}>
                Profit Distribution by Segment (₹ Crore)
              </div>
              {[
                { seg: "Index Options", val: 43289.33, color: "#51cf66" },
                { seg: "Stock Options", val: 899.99, color: "#4dabf7" },
                { seg: "Index Futures", val: -190.81, color: "#ff6b6b" },
                { seg: "Cash / Equities", val: -288.17, color: "#ff6b6b" },
                { seg: "Stock Futures", val: -7208.23, color: "#ff6b6b" },
              ].map(s => {
                const maxAbs = 43289.33;
                const w = Math.abs(s.val) / maxAbs * 100;
                return (
                  <div key={s.seg} style={{ marginBottom: 10, display: "flex", alignItems: "center", gap: 12 }}>
                    <div style={{ width: 120, fontSize: 11, color: "#aaa", fontFamily: "'JetBrains Mono', monospace", flexShrink: 0 }}>{s.seg}</div>
                    <div style={{ flex: 1, background: "#222", borderRadius: 4, height: 20, overflow: "hidden" }}>
                      <div style={{ width: `${Math.max(w, 1)}%`, height: "100%", background: s.color, borderRadius: 4, opacity: 0.7 }} />
                    </div>
                    <div style={{ width: 100, textAlign: "right", fontSize: 11, fontFamily: "'JetBrains Mono', monospace", color: s.val >= 0 ? "#51cf66" : "#ff6b6b", flexShrink: 0 }}>
                      {s.val >= 0 ? "+" : ""}₹{s.val.toLocaleString()}
                    </div>
                  </div>
                );
              })}
              <div style={{ marginTop: 12, padding: 10, background: "#222", borderRadius: 4, fontSize: 12, color: "#999" }}>
                Net: ₹36,502.12 Cr profit. The ₹7,687 Cr loss in equities/futures was the "cost" of index manipulation — losses incurred deliberately to profit enormously in index options.
              </div>
            </Card>
          </div>
        )}

        {tab === "pipeline" && (
          <div>
            <Card style={{ marginBottom: 16 }}>
              <div style={{ fontSize: 14, fontWeight: 600, color: "#f0f0f0", marginBottom: 12 }}>What You Have Now</div>
              {[
                ["SEBI Interim Order (105 pp)", "21 impugned days, 4 entity PANs, minute-level LTP tables for sample days, profit breakdowns, strategy classifications", "#51cf66"],
                ["ChatGPT Research Reports", "Entity mapping, strategy descriptions, data collection framework, RL design outline", "#4dabf7"],
                ["Extracted CSVs (this session)", "impugned_days.csv, entities_profit_loss.csv, case_timeline.csv, jan17 sample, market metrics", "#e8590c"],
              ].map(([t, d, c], i) => (
                <div key={i} style={{ padding: 12, background: "#222", borderRadius: 6, marginBottom: 8, borderLeft: `3px solid ${c}` }}>
                  <div style={{ fontSize: 13, fontWeight: 600, color: "#ddd" }}>{t}</div>
                  <div style={{ fontSize: 11, color: "#888", marginTop: 4 }}>{d}</div>
                </div>
              ))}
            </Card>

            <Card style={{ marginBottom: 16 }}>
              <div style={{ fontSize: 14, fontWeight: 600, color: "#ffd43b", marginBottom: 12 }}>Critical Gaps & Realistic Assessment</div>
              {[
                ["PAN-linked trade data", "NOT publicly available. SEBI/NSE have it; you don't. The SAT appeal may produce some but SEBI opposes broader disclosure.", "#ff6b6b"],
                ["Minute-level market data", "Need licensed NSE data or vendor feed (Truedata, Global Datafeeds, etc). Free sources give EOD only. Budget ~₹50K-2L/year for intraday.", "#ffd43b"],
                ["Full table extraction from PDF", "SEBI order has ~40+ tables. Many are image-based or complex layouts. Needs careful OCR + manual QA pipeline.", "#ffd43b"],
                ["Options chain intraday snapshots", "Critical for attribution model. Not in free data. Need tick-by-tick options data product from NSE or vendor.", "#ff6b6b"],
              ].map(([t, d, c], i) => (
                <div key={i} style={{ padding: 12, background: "#1a1a1a", borderRadius: 6, marginBottom: 8, borderLeft: `3px solid ${c}` }}>
                  <div style={{ fontSize: 13, fontWeight: 600, color: "#ddd" }}>{t}</div>
                  <div style={{ fontSize: 11, color: "#888", marginTop: 4 }}>{d}</div>
                </div>
              ))}
            </Card>

            <Card>
              <div style={{ fontSize: 14, fontWeight: 600, color: "#e8590c", marginBottom: 16 }}>Recommended Build Order</div>
              {[
                { n: "1", t: "PDF Table Extraction Pipeline", d: "Extract all 40+ tables from SEBI order into structured CSVs. Use camelot/tabula + manual QA. Priority: Tables 7-12 (LTP analysis), Table 44 (gains), Table 4 (profit summary)." },
                { n: "2", t: "Market Data Procurement", d: "License intraday index + constituent data for exam period. NSE bhavcopy archives for EOD. Vendor feed for 1-min bars. Map expiry calendar." },
                { n: "3", t: "Feature Engineering on Disclosed Days", d: "Build per-day feature vectors: last-hour vol, directional move, constituent dispersion, volume concentration. Start with the 18 exam-period days vs matched controls." },
                { n: "4", t: "Attribution Scoring Model", d: "Likelihood ratio: p(features|impugned) vs p(features|baseline). KDE or regularized GMM with leave-one-out CV. Calibrate with Platt scaling. Small positive set = conservative estimation." },
                { n: "5", t: "RL Surveillance Environment", d: "Gymnasium env for alert decisions (not trading). States = rolling features, actions = flag/escalate/pass. Reward = early detection - false positive cost. Safe framing only." },
              ].map((s, i) => (
                <div key={i} style={{ display: "flex", gap: 14, marginBottom: 14 }}>
                  <div style={{
                    width: 28, height: 28, borderRadius: "50%", background: "#e8590c",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 13, fontWeight: 700, color: "#fff", flexShrink: 0,
                    fontFamily: "'JetBrains Mono', monospace",
                  }}>{s.n}</div>
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 600, color: "#f0f0f0" }}>{s.t}</div>
                    <div style={{ fontSize: 11, color: "#888", marginTop: 2, lineHeight: 1.5 }}>{s.d}</div>
                  </div>
                </div>
              ))}
            </Card>
          </div>
        )}

        <div style={{ marginTop: 32, padding: "16px 0", borderTop: "1px solid #222", fontSize: 10, color: "#444", fontFamily: "'JetBrains Mono', monospace", textAlign: "center" }}>
          Data sourced from SEBI Interim Order WTM/AN/MRD/MRD-SEC-3/31516/2025-26 dated July 3, 2025.
          All figures are alleged; final adjudication pending. For forensic research and market surveillance purposes only.
        </div>
      </div>
    </div>
  );
}
