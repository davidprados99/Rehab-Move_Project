import React from "react";

interface DashboardCardProps {
    title: string;
    description: string;
    buttonText?: string;
    imageSrc: string;
    imageAlt: string;
    onButtonClick?: () => void;
    className?: string;
}

const DashboardCard: React.FC<DashboardCardProps> = ({
    title,
    description,
    buttonText,
    imageSrc,
    imageAlt,
    onButtonClick,
    className = "",
}) => {
    return (
        <div className={`bg-rehab-dark text-white rounded-rehab shadow-lg overflow-hidden flex flex-col md:flex-row items-center ${className}`}>
            {/* Text container */}
            <div className="p-8 flex-1">
                <h2 className="text-2xl font-bold mb-2">{title}</h2>
                <p className="text-rehab-light/80 mb-6">{description}</p>
                {buttonText && (
                    <button
                        onClick={onButtonClick}
                        className="bg-rehab-primary hover:bg-rehab-primary/90 text-white font-bold px-6 py-2 rounded-lg transition-all"
                    >
                        {buttonText}
                    </button>
                )}
            </div>

            {/* Image container */}
            <div className="w-full md:w-1/3 h-48 md:h-full min-h-[200px] relative">
                <img
                    src={imageSrc}
                    alt={imageAlt}
                    className="absolute inset-0 w-full h-full object-cover opacity-80 hover:opacity-100 transition-opacity duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t md:bg-gradient-to-l from-rehab-dark/0 to-rehab-dark" />
            </div>
        </div>
    );
};

export default DashboardCard;