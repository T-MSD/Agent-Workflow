interface AlertErrorProps {
  message?: string;
  fading?: boolean;
}

function AlertError({
  message = "Something went wrong.",
  fading = false,
}: AlertErrorProps) {
  return (
    <div
      role="alert"
      className={`bg-red-800 border-l-4 border-red-500 text-red-900 p-2 rounded-lg flex items-center transition-all duration-1000 ease-in-out hover:bg-red-800 transform hover:scale-105 ${
        fading ? "opacity-0" : "opacity-100"
      }`}
    >
      <svg
        stroke="currentColor"
        viewBox="0 0 24 24"
        fill="none"
        className="h-5 w-5 flex-shrink-0 mr-2 text-red-400"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M13 16h-1v-4h1m0-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          strokeWidth="2"
          strokeLinejoin="round"
          strokeLinecap="round"
        />
      </svg>
      <p className="text-xs font-semibold text-white flex-1">
        Error - {message}
      </p>
    </div>
  );
}

export default AlertError;
