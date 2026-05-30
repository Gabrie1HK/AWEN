import { PARCEL_STATUS_LABELS } from '../../utils/statusTranslations'

const STEP_LABELS = PARCEL_STATUS_LABELS

export default function StepperTimeline({ steps }) {
  return (
    <div className="stepper-timeline">
      {steps.map((step, i) => {
        const isActive = step.completed
        const isCurrent = !step.completed && (i === 0 || steps[i - 1]?.completed)
        return (
          <div key={step.step} className={`stepper-step ${isActive ? 'active' : ''} ${isCurrent ? 'current' : ''}`}>
            <div className="stepper-marker">
              {isActive ? (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              ) : (
                <div className="stepper-dot" />
              )}
            </div>
            <div className="stepper-content">
              <span className="stepper-label">{STEP_LABELS[step.step] || step.step}</span>
              {step.date && (
                <span className="stepper-meta">{step.date} {step.time} &middot; {step.location}</span>
              )}
              {step.operator && (
                <span className="stepper-operator">{step.operator}</span>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}
