// import SignUpForm from "./SignUpForm";
import SignUpForm from "../../Components/SignUp/SignUp";
import "./Auth.css";

function Welcome() {
  return (
    <div className="signup-container">
      <div className="signup-image-container">
        <div className="signup-overlay">
          <div className="signup-text">
            <h1>ISMS</h1>
            <h2>Inventory Management System</h2>
            <p>
              Streamline your inventory operations with our powerful management
              solution
            </p>
            <div className="features">
              <div className="feature">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                </svg>
                <span>Real-time Analytics</span>
              </div>
              <div className="feature">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                  <line x1="8" y1="21" x2="16" y2="21"></line>
                  <line x1="12" y1="17" x2="12" y2="21"></line>
                </svg>
                <span>Multi-platform Access</span>
              </div>
              <div className="feature">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
                <span>Secure Data Storage</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="signup-form-container">
        <SignUpForm />
      </div>
    </div>
  );
}

export default Welcome;
