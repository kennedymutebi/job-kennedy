import { useState } from "react";
import "./SignUp.css";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import axios from "axios";

import {
  FaBuilding,
  FaIndustry,
  FaUsers,
  FaUser,
  FaEnvelope,
  FaPhone,
  FaLock,
  FaGlobe,
  FaCity,
  FaMapMarkedAlt,
  FaFileContract,
} from "react-icons/fa";

function SignUpForm() {
  const [formData, setFormData] = useState({
    companyName: "",
    industry: "",
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
    country: "",
    city: "",
    state: "",
    employees: "",
    agreeTerms: false,
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.companyName)
      newErrors.companyName = "Company name is required";
    if (!formData.industry) newErrors.industry = "Industry is required";
    if (!formData.firstName) newErrors.firstName = "First name is required";
    if (!formData.lastName) newErrors.lastName = "Last name is required";

    if (!formData.email) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Email is invalid";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
    }

    if (!formData.agreeTerms) {
      newErrors.agreeTerms = "You must agree to the terms and conditions";
    }

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validateForm();

    if (Object.keys(newErrors).length === 0) {
      setIsSubmitting(true);

      // Prepare data for API
      const apiData = {
        company_name: formData.companyName,
        industry: formData.industry,
        first_name: formData.firstName,
        last_name: formData.lastName,
        email: formData.email,
        phone_number: formData.phone || null,
        password: formData.password,
        country: formData.country || null,
        city: formData.city || null,
        state: formData.state || null,
        num_employees: formData.employees || null,
      };

      try {
        const response = await axios.post(
          "https://kennedymutebi.pythonanywhere.com/api/v1/api/register/admin/",
          apiData,
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        // Success toast notification
        toast.success("Registration successful! You can now log in.", {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
        });

        // Reset form
        setFormData({
          companyName: "",
          industry: "",
          firstName: "",
          lastName: "",
          email: "",
          phone: "",
          password: "",
          confirmPassword: "",
          country: "",
          city: "",
          state: "",
          employees: "",
          agreeTerms: false,
        });
      } catch (error) {
        // Show error message
        const errorMessage =
          error.response?.data?.message ||
          "Registration failed. Please try again.";
        toast.error(errorMessage, {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
        });

        // Handle specific API validation errors
        if (error.response?.data?.errors) {
          const apiErrors = {};
          Object.keys(error.response.data.errors).forEach((key) => {
            // Map API error fields to form fields
            const fieldMapping = {
              company_name: "companyName",
              first_name: "firstName",
              last_name: "lastName",
              email: "email",
              phone_number: "phone",
              password: "password",
              // Add more mappings as needed
            };

            const formField = fieldMapping[key] || key;
            apiErrors[formField] = error.response.data.errors[key][0];
          });
          setErrors({ ...newErrors, ...apiErrors });
        }
      } finally {
        setIsSubmitting(false);
      }
    } else {
      setErrors(newErrors);
    }
  };

  const industryOptions = [
    "Retail",
    "Manufacturing",
    "Wholesale",
    "Healthcare",
    "Food & Beverage",
    "Technology",
    "Construction",
    "Automotive",
    "Other",
  ];

  const employeeOptions = [
    "1-10",
    "11-50",
    "51-200",
    "201-500",
    "501-1000",
    "1000+",
  ];

  return (
    <div className="form-wrapper">
      <ToastContainer />
      <h2>Create Your Account</h2>
      <p className="form-subtitle">
        Register your company to get started with ISMS
      </p>

      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <h3>
            <FaBuilding className="section-icon" />
            <span>Company Information</span>
          </h3>

          <div className="form-group">
            <label htmlFor="companyName">
              <FaBuilding className="field-icon" /> Company Name*
            </label>
            <input
              type="text"
              id="companyName"
              name="companyName"
              value={formData.companyName}
              onChange={handleChange}
              className={errors.companyName ? "error" : ""}
              placeholder="Enter company name"
            />
            {errors.companyName && (
              <span className="error-message">{errors.companyName}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="industry">
              <FaIndustry className="field-icon" /> Industry*
            </label>
            <select
              id="industry"
              name="industry"
              value={formData.industry}
              onChange={handleChange}
              className={errors.industry ? "error" : ""}
            >
              <option value="">Select Industry</option>
              {industryOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
            {errors.industry && (
              <span className="error-message">{errors.industry}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="employees">
              <FaUsers className="field-icon" /> Number of Employees
            </label>
            <select
              id="employees"
              name="employees"
              value={formData.employees}
              onChange={handleChange}
            >
              <option value="">Select Range</option>
              {employeeOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-section">
          <h3>
            <FaUser className="section-icon" />
            <span>Admin User Details</span>
          </h3>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="firstName">
                <FaUser className="field-icon" /> First Name*
              </label>
              <input
                type="text"
                id="firstName"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                className={errors.firstName ? "error" : ""}
                placeholder="Enter first name"
              />
              {errors.firstName && (
                <span className="error-message">{errors.firstName}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="lastName">
                <FaUser className="field-icon" /> Last Name*
              </label>
              <input
                type="text"
                id="lastName"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                className={errors.lastName ? "error" : ""}
                placeholder="Enter last name"
              />
              {errors.lastName && (
                <span className="error-message">{errors.lastName}</span>
              )}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="email">
              <FaEnvelope className="field-icon" /> Email Address*
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? "error" : ""}
              placeholder="Enter email address"
            />
            {errors.email && (
              <span className="error-message">{errors.email}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="phone">
              <FaPhone className="field-icon" /> Phone Number
            </label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="Enter phone number"
            />
          </div>
        </div>

        <div className="form-section">
          <h3>
            <FaLock className="section-icon" />
            <span>Security</span>
          </h3>

          <div className="form-group">
            <label htmlFor="password">
              <FaLock className="field-icon" /> Password*
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className={errors.password ? "error" : ""}
              placeholder="Enter password"
            />
            {errors.password && (
              <span className="error-message">{errors.password}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">
              <FaLock className="field-icon" /> Confirm Password*
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              className={errors.confirmPassword ? "error" : ""}
              placeholder="Confirm your password"
            />
            {errors.confirmPassword && (
              <span className="error-message">{errors.confirmPassword}</span>
            )}
          </div>
        </div>

        <div className="form-section">
          <h3>
            <FaGlobe className="section-icon" />
            <span>Address Information</span>
          </h3>

          <div className="form-group">
            <label htmlFor="country">
              <FaGlobe className="field-icon" /> Country
            </label>
            <input
              type="text"
              id="country"
              name="country"
              value={formData.country || ""}
              onChange={handleChange}
              placeholder="Enter country"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="city">
                <FaCity className="field-icon" /> City
              </label>
              <input
                type="text"
                id="city"
                name="city"
                value={formData.city}
                onChange={handleChange}
                placeholder="Enter city"
              />
            </div>

            <div className="form-group">
              <label htmlFor="state">
                <FaMapMarkedAlt className="field-icon" /> State
              </label>
              <input
                type="text"
                id="state"
                name="state"
                value={formData.state}
                onChange={handleChange}
                placeholder="Enter state"
              />
            </div>
          </div>
        </div>

        <div className="form-group checkbox-group">
          <input
            type="checkbox"
            id="agreeTerms"
            name="agreeTerms"
            checked={formData.agreeTerms}
            onChange={handleChange}
            className={errors.agreeTerms ? "error" : ""}
          />
          <label htmlFor="agreeTerms">
            <FaFileContract className="field-icon" />I agree to the{" "}
            <a href="#terms">Terms and Conditions</a> and{" "}
            <a href="#privacy">Privacy Policy</a>
          </label>
          {errors.agreeTerms && (
            <span className="error-message">{errors.agreeTerms}</span>
          )}
        </div>

        <button type="submit" className="submit-button" disabled={isSubmitting}>
          {isSubmitting ? (
            <span className="loading-spinner">
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
                className="animate-spin"
              >
                <circle cx="12" cy="12" r="10" opacity="0.25"></circle>
                <path d="M12 2a10 10 0 0 1 10 10" opacity="1"></path>
              </svg>
              Processing...
            </span>
          ) : (
            "Create Account"
          )}
        </button>

        <p className="login-link">
          Already have an account? <a href="#login">Log in</a>
        </p>
      </form>
    </div>
  );
}

export default SignUpForm;
