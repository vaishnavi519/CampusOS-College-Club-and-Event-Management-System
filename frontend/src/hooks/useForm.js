import { useCallback, useRef, useState } from 'react';
import { validate } from '../utils/validation.js';

export function useForm({ initialValues, schema = {}, onSubmit }) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);

  const schemaRef = useRef(schema);
  schemaRef.current = schema;

  const setValue = useCallback((name, value) => {
    setValues((previous) => {
      const next = { ...previous, [name]: value };
      return next;
    });

    const rules = schemaRef.current[name];

    if (rules) {
      setErrors((previousErrors) => {
        if (!previousErrors[name] && !touched[name]) {
          return previousErrors;
        }

        const message = validate(
          { ...values, [name]: value },
          { [name]: rules },
        )[name];

        const updated = { ...previousErrors };

        if (message) {
          updated[name] = message;
        } else {
          delete updated[name];
        }

        return updated;
      });
    }
  }, [values, touched]);

  const handleChange = useCallback((event) => {
    const { name, value, type, checked } = event.target;
    setValue(name, type === 'checkbox' ? checked : value);
  }, [setValue]);

  const handleBlur = useCallback((event) => {
  const { name } = event.target;

  setTouched((previous) => ({
    ...previous,
    [name]: true,
  }));
  }, []);

   

  const handleSubmit = useCallback(async (event) => {
    event?.preventDefault?.();
    setSubmitError(null);

    const currentSchema = schemaRef.current;
    const fieldNames = Object.keys(currentSchema);
    const found = validate(values, currentSchema);

    console.log('[Register] Values:', values);
    console.log('[Register] Validation results:', found);

    setErrors(found);

    setTouched(
      Object.fromEntries(fieldNames.map((name) => [name, true])),
    );

    if (Object.keys(found).length > 0) {
      return;
    }

    setSubmitting(true);

    try {
      await onSubmit(values);
    } catch (error) {
      setSubmitError(error);
    } finally {
      setSubmitting(false);
    }
  }, [values, onSubmit]);

  const field = useCallback((name) => ({
    name,
    value: values[name] ?? '',
    onChange: handleChange,
    onBlur: handleBlur,
    error: errors[name] || undefined,
  }), [values, errors, handleChange, handleBlur]);

  return {
    values,
    errors,
    touched,
    submitting,
    submitError,
    setValue,
    setValues,
    setSubmitError,
    handleChange,
    handleBlur,
    handleSubmit,
    field,
  };
}
