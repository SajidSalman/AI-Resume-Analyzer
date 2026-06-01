import { useState } from "react";
import {
  CircularProgressbar,
  buildStyles,
} from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [resumeId, setResumeId] = useState(null);
  const [resumePreview, setResumePreview] = useState("");
  const [companyName, setCompanyName] = useState("infosys");

  const [result, setResult] = useState(null);
  const [companyResult, setCompanyResult] = useState(null);
  const [atsFeedback, setAtsFeedback] = useState([]);
  const [projectResult, setProjectResult] = useState([]);

  const [loading, setLoading] = useState(false);
  const [uploadSuccess, setUploadSuccess] =
    useState(false);
  const [error, setError] = useState("");

  const score = result?.match_score || 0;

  const glass = {
    background: "rgba(30,41,59,0.9)",
    backdropFilter: "blur(10px)",
    borderRadius: "18px",
    padding: "18px",
    border: "1px solid rgba(255,255,255,0.08)",
    boxShadow: "0 8px 25px rgba(0,0,0,0.25)",
    transition: "all 0.25s ease",
  };

  const badge = (text, color) => (
    <span
      key={text}
      style={{
        display: "inline-block",
        padding: "8px 14px",
        margin: "6px",
        borderRadius: "999px",
        background: color,
        fontSize: "14px",
      }}
    >
      {text}
    </span>
  );

  const statCard = (title, value, color) => (
    <div style={{ ...glass, textAlign: "center" }}>
      <h3>{title}</h3>

      <div
        style={{
          fontSize: "32px",
          fontWeight: "700",
          color,
          marginTop: "12px",
        }}
      >
        {value}
      </div>
    </div>
  );

  const uploadAndAnalyze = async () => {
    if (!resumeFile || !jobDescription) {
      alert("Upload resume + paste JD");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const formData = new FormData();
      formData.append("file", resumeFile);

      const upload = await fetch(
        "http://127.0.0.1:8000/upload-resume",
        {
          method: "POST",
          body: formData,
        }
      );

      const uploadData = await upload.json();

      const id = uploadData.resume_id;

      setResumeId(id);
      setUploadSuccess(true);
      setResumePreview(uploadData.preview || "");

      const analyze = await fetch(
        `http://127.0.0.1:8000/analyze?resume_id=${id}&job_description=${encodeURIComponent(
          jobDescription
        )}`,
        { method: "POST" }
      );

      setResult(await analyze.json());

      const ats = await fetch(
        `http://127.0.0.1:8000/ats-feedback?resume_id=${id}&job_description=${encodeURIComponent(
          jobDescription
        )}`,
        { method: "POST" }
      );

      setAtsFeedback(await ats.json());
    } catch {
      setError(
        "Something went wrong. Try again."
      );
    }

    setLoading(false);
  };

  const handleCompanyFit = async () => {
    const res = await fetch(
      `http://127.0.0.1:8000/company-fit?resume_id=${resumeId}&company_name=${companyName}`,
      { method: "POST" }
    );

    setCompanyResult(await res.json());
  };

  const handleProjects = async () => {
    const res = await fetch(
      `http://127.0.0.1:8000/project-score?resume_id=${resumeId}`,
      { method: "POST" }
    );

    setProjectResult(await res.json());
  };

  const exportReport = () => {
    window.print();
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "grid",
        gridTemplateColumns: "320px 1fr",
        background:
          "linear-gradient(135deg,#020617,#0f172a,#111827)",
        color: "white",
        fontFamily: "Inter, Arial",
      }}
    >
      {/* sidebar */}

      <div
        style={{
          padding: "24px",
          borderRight:
            "1px solid rgba(255,255,255,0.08)",
          background: "rgba(15,23,42,0.96)",
          overflowY: "auto",
        }}
      >
        <h2
          style={{
            fontSize: "28px",
            marginBottom: "20px",
          }}
        >
          Resume Analyzer
        </h2>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) =>
            setResumeFile(e.target.files[0])
          }
        />

        {resumeFile && (
          <div
            style={{
              marginTop: "10px",
              color: "#cbd5e1",
            }}
          >
            {resumeFile.name}
          </div>
        )}

        {uploadSuccess && (
          <div
            style={{
              color: "#22c55e",
              marginTop: "10px",
            }}
          >
            Resume uploaded successfully
          </div>
        )}

        {error && (
          <div
            style={{
              color: "#ef4444",
              marginTop: "10px",
            }}
          >
            {error}
          </div>
        )}

        {resumePreview && (
          <div
            style={{
              marginTop: "18px",
              background: "#1e293b",
              padding: "14px",
              borderRadius: "12px",
              fontSize: "12px",
              lineHeight: "1.5",
              maxHeight: "170px",
              overflowY: "auto",
              whiteSpace: "pre-wrap",
            }}
          >
            {resumePreview}
          </div>
        )}

        <br />

        <textarea
          rows="8"
          placeholder="Paste Job Description"
          value={jobDescription}
          onChange={(e) =>
            setJobDescription(e.target.value)
          }
          style={{
            width: "100%",
            padding: "14px",
            borderRadius: "12px",
            background: "#1e293b",
            color: "white",
            border: "none",
          }}
        />

        <br />
        <br />

        <button
          disabled={loading}
          onClick={uploadAndAnalyze}
          style={{
            width: "100%",
            padding: "14px",
            borderRadius: "12px",
            border: "none",
            background: loading
              ? "#475569"
              : "#2563eb",
            color: "white",
            cursor: loading
              ? "not-allowed"
              : "pointer",
          }}
        >
          {loading
            ? "Analyzing..."
            : "Analyze Resume"}
        </button>

        <br />
        <br />

        <select
          value={companyName}
          onChange={(e) =>
            setCompanyName(e.target.value)
          }
          style={{
            width: "100%",
            padding: "12px",
            borderRadius: "12px",
          }}
        >
          <option value="infosys">Infosys</option>
          <option value="amazon">Amazon</option>
          <option value="google">Google</option>
          <option value="tcs">TCS</option>
        </select>

        <br />
        <br />

        <button
          onClick={handleCompanyFit}
          style={{
            width: "100%",
            padding: "14px",
            borderRadius: "12px",
            border: "none",
            background: "#3b82f6",
            color: "white",
          }}
        >
          Check Company Fit
        </button>

        <br />
        <br />

        <button
          onClick={handleProjects}
          style={{
            width: "100%",
            padding: "14px",
            borderRadius: "12px",
            border: "none",
            background: "#16a34a",
            color: "white",
          }}
        >
          Analyze Projects
        </button>
      </div>

      {/* dashboard */}

      <div
        style={{
          padding: "40px",
        }}
      >
        <h1
          style={{
            fontSize: "38px",
            textAlign: "center",
          }}
        >
          Resume Insights Dashboard
        </h1>

        <p
          style={{
            textAlign: "center",
            color: "#cbd5e1",
            marginBottom: "28px",
          }}
        >
          Smart ATS analysis powered by AI
        </p>

        {!result && (
          <div
            style={{
              ...glass,
              textAlign: "center",
            }}
          >
            Upload resume and paste
            job description to start
          </div>
        )}

        {result && (
          <>
            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(4,1fr)",
                gap: "18px",
              }}
            >
              <div style={glass}>
                <h3
                  style={{
                    textAlign: "center",
                  }}
                >
                  ATS Score
                </h3>

                <div
                  style={{
                    width: "110px",
                    margin: "auto",
                  }}
                >
                  <CircularProgressbar
                    value={score}
                    text={`${score}%`}
                    styles={buildStyles({
                      pathColor: "#22c55e",
                      textColor: "#fff",
                      trailColor: "#334155",
                    })}
                  />
                </div>
              </div>

              {statCard(
                "Company Fit",
                companyResult
                  ? `${companyResult.fit_score}%`
                  : "--",
                "#60a5fa"
              )}

              {statCard(
                "Matched",
                result.matched_skills?.length || 0,
                "#22c55e"
              )}

              {statCard(
                "Missing",
                result.missing_skills?.length || 0,
                "#ef4444"
              )}
            </div>

            <br />

            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "1fr 1fr",
                gap: "18px",
              }}
            >
              <div style={glass}>
                <h2>Matched Skills</h2>

                {result.matched_skills?.map((s) =>
                  badge(s, "#14532d")
                )}
              </div>

              <div style={glass}>
                <h2>Missing Skills</h2>

                {result.missing_skills?.map((s) =>
                  badge(s, "#7f1d1d")
                )}
              </div>
            </div>

            <br />

            <div style={glass}>
              <h2>ATS Feedback</h2>

              {atsFeedback.map((tip, i) => (
                <div key={i}>
                  • {tip}
                </div>
              ))}

              <br />

              <button
                onClick={() =>
                  navigator.clipboard.writeText(
                    atsFeedback.join("\n")
                  )
                }
                style={{
                  padding: "10px",
                  borderRadius: "10px",
                  border: "none",
                }}
              >
                Copy Feedback
              </button>
            </div>

            <br />

            <div style={glass}>
              <h2>Top Recommendations</h2>

              <div>
                ✅ Add measurable achievements
              </div>

              <div>
                ✅ Add GitHub links
              </div>

              <div>
                ✅ Mention deployment/demo
              </div>
            </div>

            <br />

            <div style={glass}>
              <h2>Resume Summary</h2>

              <p>
                ATS score {score}%.
                Matched:
                {" "}
                {result.matched_skills?.length}
                {" "}
                Missing:
                {" "}
                {result.missing_skills?.length}
              </p>
            </div>


            <br />

            <h2>Projects</h2>

            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fit,minmax(250px,1fr))",
                gap: "18px",
              }}
            >
              {projectResult.length === 0 && (
                <div style={glass}>
                  Click Analyze Projects
                  to view project insights
                </div>
              )}

              {projectResult.map((p, i) => (
                <div
                  key={i}
                  style={{
                    ...glass,
                    minHeight: "180px",
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform =
                      "translateY(-4px)";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform =
                      "translateY(0)";
                  }}
                >
                  <h3>{p.project}</h3>

                  <p>
                    Score: {p.score}/10
                  </p>

                  <div
                    style={{
                      background: "#334155",
                      height: "8px",
                      borderRadius: "8px",
                    }}
                  >
                    <div
                      style={{
                        width: `${p.score * 10}%`,
                        height: "8px",
                        borderRadius: "8px",
                        background: "#3b82f6",
                      }}
                    />
                  </div>

                  <br />

                  {p.tips?.map((tip, idx) => (
                    <div key={idx}>
                      • {tip}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </>
        )}<br />

        <button
          onClick={exportReport}
          style={{
            padding: "12px",
            borderRadius: "12px",
            border: "none",
            background: "#9333ea",
            color: "white",
          }}
        >
          Export Report
        </button>

        <br />
      </div>
    </div>
  );
}

export default App;